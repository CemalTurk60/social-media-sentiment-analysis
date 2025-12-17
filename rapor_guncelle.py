import pandas as pd
from datetime import datetime

# Dosyalar
GIRIS_DOSYASI = "bert_analiz_sonuclari.xlsx"
CIKIS_RAPORU = "profesyonel_analiz_raporu.txt"

def raporu_yenile():
    print("🔄 Rapor güncelleniyor...")
    
    try:
        df = pd.read_excel(GIRIS_DOSYASI)
    except FileNotFoundError:
        print("❌ Hata: Analiz dosyası bulunamadı!")
        return

    # --- İSTATİSTİKLERİ HESAPLA ---
    toplam_yorum = len(df)
    
    # BERT Sonuçlarını Say
    dagilim = df['BERT_Etiket'].value_counts()
    olumlu = dagilim.get('Olumlu', 0)
    olumsuz = dagilim.get('Olumsuz', 0)
    
    # Oranlar
    olumlu_oran = (olumlu / toplam_yorum) * 100
    olumsuz_oran = (olumsuz / toplam_yorum) * 100

    # Tarih
    bugun = datetime.now().strftime("%Y-%m-%d %H:%M")

    # --- RAPOR METNİ ---
    rapor_icerigi = f"""
================================================
PROJE ANALİZ RAPORU (GÜNCEL - FAZ 2)
Tarih: {bugun}
================================================

1. GENEL İSTATİSTİKLER (GÜNCELLENDİ)
----------------------
Toplam Analiz Edilen Yeri: {toplam_yorum} Adet
Kapsam: Çoklu Ürün (iPhone, Samsung, Dyson vb.) + Sosyal Medya Simülasyonu

2. YAPAY ZEKA (BERT) SONUÇLARI
--------------------------
🟢 Olumlu Yorumlar: {olumlu} (%{olumlu_oran:.1f})
🔴 Olumsuz Yorumlar: {olumsuz} (%{olumsuz_oran:.1f})

Dikkat: Olumsuz yorum sayısındaki artış, modelin şikayetleri
başarıyla tespit ettiğini ve simülasyon verilerinin (Twitter) etkisini gösterir.

3. KULLANILAN TEKNOLOJİ
--------------------
Eski Yöntem: Sözlük Tabanlı (İPTAL EDİLDİ)
Yeni Yöntem: Hugging Face BERT (Derin Öğrenme)
Model Adı: savasy/bert-base-turkish-sentiment-cased

4. SONUÇ VE ÖNERİ
-----------------
Bu analiz, sadece kelimeleri sayan basit yöntemler yerine,
cümlenin bağlamını anlayan BERT modeli ile yapılmıştır.
Elde edilen {olumsuz} adet olumsuz geri bildirim, firmalar için
kritik Ar-Ge verisi niteliğindedir.

================================================
Cemalettin Türk - YBS Bitirme Projesi
"""

    # Dosyayı Kaydet (Eskisinin üzerine yazar)
    with open(CIKIS_RAPORU, "w", encoding="utf-8") as f:
        f.write(rapor_icerigi)

    print(f"✅ YENİ RAPOR OLUŞTURULDU: {CIKIS_RAPORU}")
    print("📄 İçeriği kontrol edebilirsin.")

if __name__ == "__main__":
    raporu_yenile()