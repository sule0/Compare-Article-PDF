# 📚 Makale-Kitap Karşılaştırma Aracı

Bu proje, kitaplar ve makaleler arasında içerik karşılaştırması yapan bir araçtır. Makale içeriklerinin kitapta yer alıp almadığını kontrol eder ve detaylı bir rapor oluşturur.

## 🚀 Özellikler

- PDF ve DOCX formatında kitap dosyası desteği
- ZIP içinde birden fazla makale dosyası (.docx veya .pdf) işleme
- İki farklı karşılaştırma modu:
  - Madde madde karşılaştırma
  - Paragraf paragraf karşılaştırma
- Semantik benzerlik analizi
- Yazım benzerliği kontrolü
- HTML ve CSV formatında detaylı raporlama
- Kullanıcı dostu Streamlit arayüzü

## 💻 Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullanici_adi/comporasion_project.git
cd comporasion_project
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

3. Projeyi çalıştırın:
```bash
streamlit run streamlit_ui/app.py
```

## 🔧 Kullanım

1. Web arayüzünde karşılaştırma tipini seçin (Madde Madde veya Paragraf Paragraf)
2. Kitap dosyasını yükleyin (PDF veya DOCX formatında)
3. Makaleleri içeren ZIP dosyasını yükleyin
4. Sonuçları HTML veya CSV formatında indirin

## 📊 Çıktılar

- **HTML Raporu**: Eksik içeriklerin detaylı görsel raporu
- **CSV Raporu**: Eksik içeriklerin tablo formatında dökümü

## 🔍 Nasıl Çalışır?

1. Dokümanlardan metin çıkarılır
2. Metinler seçilen yönteme göre bölümlere ayrılır
3. Her bölüm için semantik analiz yapılır
4. Benzerlik skorları hesaplanır
5. Sonuçlar raporlanır

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 