# utils/semantic_compare.py
from sentence_transformers import util

def paragraf_benzet(model, kitap_paragraflari, kitap_embeddings, makale_paragraflari, makale_embeddings, esik=0.75):
    """
    Her makale paragrafını kitap paragraf embedding'leri ile karşılaştırır.
    Eşik değerinin altındaysa 'eksik bilgi' olarak döner.
    """
    eksik_bilgiler = []

    for i, m_embed in enumerate(makale_embeddings):
        benzerlikler = util.pytorch_cos_sim(m_embed, kitap_embeddings)[0]  # kitap embedding’lerine karşılaştır
        en_yuksek_skor = benzerlikler.max().item()
        
        if en_yuksek_skor < esik:
            eksik_bilgiler.append({
                "makale_paragraf": makale_paragraflari[i],
                "en_yakin_skor": round(en_yuksek_skor, 3)
            })

    return eksik_bilgiler


def makale_kitap_ortalama_benzerlik(makale_embedding, kitap_embeddings):
    """
   maksimum benzerlik skorlarını döner.
    """
    skorlar = util.pytorch_cos_sim(makale_embedding, kitap_embeddings)[0]
    return skorlar.max().item()

from rapidfuzz import fuzz

def yazim_benzerligi_kontrolu(madde, kitap_paragraflari, esik=85):
    """
    Madde metninin kitap paragraflarına harf bazında benzerliğini kontrol eder.
    Maksimum string benzerlik skorunu döner.
    """
    skorlar = [fuzz.token_set_ratio(madde, kitap_paragraf) for kitap_paragraf in kitap_paragraflari]
    return max(skorlar)
