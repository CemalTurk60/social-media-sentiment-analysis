# 📊 Product Sentiment Analysis & Dashboard (Tez Projesi)

Bu proje, sosyal medya verilerini (YouTube) analiz ederek teknolojik ürünler hakkında **Tüketici Duygu Analizi (Sentiment Analysis)** gerçekleştiren kapsamlı bir veri bilimi çalışmasıdır.

![Dashboard Önizleme](profesyonel_dashboard.png)

## 🚀 Proje Durumu: FAZ 2 (TAMAMLANDI) ✅

Proje, temel analizden **Derin Öğrenme (Deep Learning)** aşamasına geçmiştir.

### ✅ Tamamlanan Özellikler (Hafta 1 & 2)
- **Çoklu Ürün Veri Madenciliği:** YouTube API ile 5 farklı ürünün (iPhone 15, S24 vb.) verileri otomatik çekilmektedir.
- **Sosyal Medya Simülasyonu:** Instagram ve Twitter verileri, istatistiksel yöntemlerle simüle edilerek veri seti 2000+ satıra çıkarılmıştır.
- **Hibrit Yapay Zeka Mimarisi:**
  - **Model 1 (Baseline):** Logistic Regression (Makine Öğrenmesi) - %82 Doğruluk.
  - **Model 2 (Advanced):** **BERT (bert-base-turkish-sentiment-cased)** modeli ile bağlam duyarlı derin analiz.
- **Veri Tabanı Mimarisi:** SQLite ve Excel entegrasyonu.

## 🛠️ Teknoloji Yığını
| Alan | Teknoloji | Kullanım Amacı |
|------|-----------|----------------|
| **AI / ML** | **PyTorch, Transformers (BERT)** | Derin Öğrenme ve Duygu Analizi |
| **Model** | Scikit-Learn | Lojistik Regresyon ve TF-IDF |
| **Dil** | Python 3.12 | Ana geliştirme dili |
| **Veri** | Pandas, NumPy | Veri manipülasyonu ve temizlik |
| **Görsel**| Seaborn, Matplotlib | Veri görselleştirme |

## 📊 Analiz Süreci
1. **Data Ingestion:** YouTube yorumları çekilir + Sosyal medya verileri simüle edilir.
2. **Preprocessing:** Stop-words temizliği, NLP teknikleri.
3. **AI Analysis:** Veriler BERT modelinden geçirilerek "Olumlu/Olumsuz" olarak etiketlenir.
4. **Reporting:** Sonuçlar Excel ve Veritabanına işlenir.

## 🔜 Gelecek Hedefler (Faz 3)
- [ ] **Streamlit Dashboard:** Tüm verilerin web arayüzünde sunulması.
- [ ] **Rakip Analizi:** iPhone vs Samsung karşılaştırma grafikleri.
- [ ] **Canlı Filtreleme:** Platform bazlı (Twitter/Instagram/YouTube) filtreler.

---
*Geliştirici: Cemalettin Türk | Yönetim Bilişim Sistemleri*