import streamlit as st
import tempfile
import os
import shutil
import sys
import html
import csv
import unicodedata
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.extract_pdf import extract_text_from_pdf
from utils.extract_docx import extract_all_docx_from_folder, fix_filename
from embeddings.model_loader import load_model
from embeddings.embedding_generator import metni_paragraflara_bol, bol_maddelere_ayir, paragraflari_embed_et
from utils.semantic_compare import makale_kitap_ortalama_benzerlik, yazim_benzerligi_kontrolu

# Eğer fix_filename tanımlı değilse:
def fix_filename(name):
    return unicodedata.normalize("NFC", name)

st.set_page_config(page_title="Makale-Kitap Karşılaştırma", layout="wide")
st.title("📚 Makale-Kitap Karşılaştırma Aracı")

# Yeni: Karşılaştırma tipi seçimi
ayirma_tipi = st.radio(
    "🧾 Word dosyaları nasıl yazılmış?",
    ["Madde Madde", "Paragraf Paragraf"]
)

# Session state'i başlat
if 'html_rapor' not in st.session_state:
    st.session_state.html_rapor = None
if 'csv_output' not in st.session_state:
    st.session_state.csv_output = None
if 'eksik_var_mi' not in st.session_state:
    st.session_state.eksik_var_mi = False

pdf_file = st.file_uploader("📘 Kitap (PDF veya Word)", type=["pdf", "docx"])
zip_file = st.file_uploader("📄 Makaleler (ZIP, içinde .docx veya .pdf dosyaları)", type=["zip"])



if pdf_file and zip_file and ayirma_tipi:
    with st.spinner("İşleniyor..."):
        temp_dir = tempfile.mkdtemp()

        # Kitap dosyası
        kitap_path = os.path.join(temp_dir, "kitap" + (".pdf" if pdf_file.type == "application/pdf" else ".docx"))
        with open(kitap_path, "wb") as f:
            f.write(pdf_file.read())

        # ZIP
        zip_path = os.path.join(temp_dir, "makaleler.zip")
        with open(zip_path, "wb") as f:
            f.write(zip_file.read())
        shutil.unpack_archive(zip_path, temp_dir)

        # Makaleleri çıkar
        makaleler = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(('.docx', '.pdf')):
                    file_path = os.path.join(root, file)
                    if file.endswith('.docx'):
                        makale_metin = extract_all_docx_from_folder(temp_dir, single_file=file_path)[0]["text"]
                    else:
                        makale_metin = extract_text_from_pdf(file_path)
                    makaleler.append({
                        "filename": file,
                        "text": makale_metin
                    })

        model = load_model()

        # Kitap metnini çıkar
        if pdf_file.type == "application/pdf":
            kitap_metin = extract_text_from_pdf(kitap_path)
        else:
            kitap_metin = extract_all_docx_from_folder(temp_dir, single_file=kitap_path)[0]["text"]

        kitap_paragraflari = metni_paragraflara_bol(kitap_metin)
        kitap_embeddings = paragraflari_embed_et(model, kitap_paragraflari)

        html_rapor = """
        <!DOCTYPE html>
        <html lang="tr"><head><meta charset="UTF-8"><title>Eksik Bilgi Raporu</title>
        <style>
        body { font-family: Arial; padding: 30px; background: #f9f9f9; }
        .makale { background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 40px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
        .madde { background: #ffecec; padding: 10px; margin: 10px 0; border-left: 5px solid #dc3545; }
        .madde.ok { background: #e6ffe6; border-left-color: #28a745; }
        .tam-icerik { background: #eef; padding: 10px; border-radius: 5px; margin-top: 20px; font-style: italic; }
        .etiket { font-size: 13px; color: #999; }
        </style></head><body><h1>📋 Eksik Bilgi Raporu</h1>
        """

        csv_output = StringIO()
        csv_writer = csv.writer(csv_output, lineterminator="\n")
        csv_writer.writerow(['Dosya Adı', 'Eksik Paragraf'])

        eksik_var_mi = False

        for makale in makaleler:
            if ayirma_tipi == "Madde Madde":
                maddeler = bol_maddelere_ayir(makale["text"])[1:]  # başlığı atla
            else:
                maddeler = metni_paragraflara_bol(makale["text"])

            madde_embeddings = paragraflari_embed_et(model, maddeler)
            eksik_maddeler = []

            for i, (madde, m_embed) in enumerate(zip(maddeler, madde_embeddings), start=1):
                maks = makale_kitap_ortalama_benzerlik(m_embed, kitap_embeddings)
                yazim_sk = None
                durum = "EKSİK"

                if maks >= 0.75:
                    durum = "VAR"
                else:
                    yazim_sk = yazim_benzerligi_kontrolu(madde, kitap_paragraflari)
                    if yazim_sk >= 90:
                        durum = "VAR"
                    elif yazim_sk >= 85:
                        durum = "YAZIMLA VAR"

                if durum != "VAR":
                    eksik_maddeler.append((i, maks, yazim_sk, madde.strip()))

            if eksik_maddeler:
                eksik_var_mi = True
                dosya_adi = fix_filename(makale["filename"])
                html_rapor += f'<div class="makale"><h2>📄 {html.escape(dosya_adi)}</h2>'
                html_rapor += f'<p class="etiket">{len(eksik_maddeler)} eksik madde tespit edildi</p>'

                for madde_no, maks, yazim_sk, text in eksik_maddeler:
                    html_rapor += f'<div class="madde">'
                    html_rapor += f"<strong>Madde {madde_no}</strong> / Maks: {round(maks,3)}"
                    if yazim_sk:
                        html_rapor += f" / Yazım: {round(yazim_sk)}"
                    html_rapor += f"<br>{html.escape(text[:1000])}</div>"

                    csv_writer.writerow([dosya_adi, text.strip()])

                tam_icerik = html.escape(makale["text"]).replace("\n", "<br>")
                html_rapor += f'<div class="tam-icerik"><strong>📜 Makalenin Tam İçeriği:</strong><br><br>{tam_icerik}</div></div>'

        html_rapor += "</body></html>"

        # Sonuçları session state'e kaydet
        st.session_state.html_rapor = html_rapor
        st.session_state.csv_output = csv_output
        st.session_state.eksik_var_mi = eksik_var_mi

        if eksik_var_mi:
            st.success("Eksik bilgiler tespit edildi!")

# İndirme butonlarını session state'ten gelen verilerle göster
if st.session_state.html_rapor and st.session_state.eksik_var_mi:
    st.download_button(
        "📥 HTML Raporu İndir",
        data=st.session_state.html_rapor.encode("utf-8"),
        file_name="eksik_bilgi_raporu.html",
        mime="text/html"
    )

    csv_bytes = '\ufeff' + st.session_state.csv_output.getvalue()
    st.download_button(
        "📊 Eksik Bilgileri CSV Olarak İndir",
        data=csv_bytes.encode("utf-8"),
        file_name="eksik_bilgiler.csv",
        mime="text/csv"
    )
elif st.session_state.html_rapor and not st.session_state.eksik_var_mi:
    st.info("🎉 Tüm içerikler kitapta mevcut görünüyor, eksik bilgi tespit edilmedi.")
