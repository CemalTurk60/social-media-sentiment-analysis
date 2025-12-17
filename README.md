# 📱 Ürün Yorumları Duygu Analizi: Geleneksel Yöntemden Yapay Zekaya Geçiş

Bu proje, e-ticaret yorumlarını analiz etmek için başlatılmış, süreç içerisinde **Basit Makine Öğrenmesi** yöntemlerinden **İleri Seviye Derin Öğrenme (BERT)** teknolojisine evrilmiş kapsamlı bir veri bilimi çalışmasıdır.

---

## 📅 FAZ 1: Başlangıç (Geleneksel Yöntem)
Projenin ilk aşamasında sözlük tabanlı yöntemler ve Lojistik Regresyon kullanılmıştır.
* **Yaklaşım:** Kelime sayma (Lexicon-based).
* **Sonuç:** %82 Başarı.
* **Eksiklik:** "Güzel değil" cümlesini "Güzel" kelimesinden dolayı olumlu sanıyordu.

**🔻 V1 - İlk Analiz Grafiği:**
![Eski Versiyon](dashboard_v1_eski.png)

---

## 🚀 FAZ 2: Final (Yapay Zeka & BERT Devrimi)
Hataları gidermek için proje **Hugging Face BERT** modeli ile yeniden tasarlandı.
* **Yaklaşım:** Cümlenin bağlamını (Context) anlayan Yapay Zeka.
* **Yenilik:** Twitter/Instagram simülasyonu eklendi.
* **Teknoloji:** Streamlit ile İnteraktif Dashboard kuruldu.

**🔻 V2 - Profesyonel Analiz Paneli (Final):**
![Final Versiyon](dashboard_v2_final.png)

---

## 📊 Proje Özellikleri
1.  **Çoklu Veri Çekimi:** iPhone, Samsung, Dyson vb.
2.  **Akıllı Duygu Analizi:** * ✅ "Telefon güzel değil" -> **Olumsuz** (Doğru tespit)
    * ✅ Güven Skoru hesaplama.
3.  **Canlı Dashboard:** Ürün filtreleme ve dinamik grafikler.

## 📂 Kurulum
```bash
pip install -r requirements.txt
streamlit run dashboard.py

*Geliştirici: Cemalettin Türk | Yönetim Bilişim Sistemleri*