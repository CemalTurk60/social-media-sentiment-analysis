# 📊 Product Sentiment Analysis & Dashboard (Tez Projesi)

Bu proje, sosyal medya verilerini (YouTube) analiz ederek teknolojik ürünler hakkında **Tüketici Duygu Analizi (Sentiment Analysis)** gerçekleştiren kapsamlı bir veri bilimi çalışmasıdır.

![Dashboard Önizleme](profesyonel_dashboard.png)

## 🚀 Proje Durumu: FAZ 1 (TAMAMLANDI)

Bu aşamada **ETL (Extract, Transform, Load)** süreci ve temel analiz motoru başarıyla kurulmuştur.

### ✅ Tamamlanan Özellikler
- **Veri Madenciliği:** YouTube Data API v3 ile büyük veri setlerinin otomatik çekilmesi (Pagination algoritması ile).
- **Veri Tabanı Mimarisi:** Çekilen ve işlenen verilerin **SQLite** veritabanında yapısal olarak saklanması.
- **NLP Motoru (v1.0):** Türkçe için özel geliştirilmiş **Sözlük Tabanlı (Dictionary-Based)** duygu analizi algoritması.
- **Görselleştirme:** Seaborn ve Matplotlib kullanılarak oluşturulan 6 panelli Yönetici Dashboard'u.
- **Otomatik Raporlama:** Her analiz sonrası `.txt` formatında yönetici özeti çıkarma.

## 🛠️ Teknoloji Yığını
| Alan | Teknoloji | Kullanım Amacı |
|------|-----------|----------------|
| **Dil** | Python 3.12 | Ana geliştirme dili |
| **Veri** | Pandas, NumPy | Veri manipülasyonu ve temizlik |
| **NLP** | Regex, Custom Lexicon | Metin işleme ve duygu skorlama |
| **DB** | SQLite3 | Veri saklama ve sorgulama |
| **Görsel**| Seaborn, Matplotlib | Veri görselleştirme |
| **API** | Google Client Lib | Veri çekme servisi |

## 📊 Analiz Metodolojisi
1. **Data Ingestion:** Video ID üzerinden tüm yorumlar çekilir.
2. **Preprocessing:** Stop-words temizliği, noktalama işaretleri ve lowercase dönüşümü.
3. **Scoring:** Pozitif/Negatif kelime havuzuna göre `Polarity Score` (-1 ile +1 arası) hesaplanır.
4. **Storage:** İşlenen veri SQL tablosuna `INSERT` edilir.

## 🔜 Gelecek Hedefler (Faz 2)
- [ ] BERT (Bidirectional Encoder Representations) modelinin entegrasyonu.
- [ ] Web Arayüzü (Streamlit) ile canlı kullanım.
- [ ] Rakip analizi modülü.

---
*Geliştirici: Cemalettin Türk | Yönetim Bilişim Sistemleri*