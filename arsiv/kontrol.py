import pandas as pd
import os

DOSYA_ADI = "bert_analiz_sonuclari.xlsx"

def check_up_yap():
    print("\n🩺 PROJE SAĞLIK KONTROLÜ BAŞLIYOR...\n")
    print("-" * 40)

    # 1. Dosya Varlığı Kontrolü
    if not os.path.exists(DOSYA_ADI):
        print(f"❌ KRİTİK HATA: {DOSYA_ADI} bulunamadı!")
        return
    else:
        boyut = os.path.getsize(DOSYA_ADI) / 1024 / 1024 # MB cinsinden
        print(f"✅ Dosya Mevcut: {DOSYA_ADI}")
        print(f"📦 Dosya Boyutu: {boyut:.2f} MB (Dolu görünüyor)")

    # 2. Veri İçeriği Kontrolü
    try:
        df = pd.read_excel(DOSYA_ADI)
        toplam_veri = len(df)
        print(f"📊 Toplam Satır Sayısı: {toplam_veri}")
        
        if toplam_veri < 100:
            print("⚠️ UYARI: Veri sayısı çok az!")
        else:
            print("✅ Veri hacmi yeterli.")

    except Exception as e:
        print(f"❌ Dosya okunamadı: {e}")
        return

    # 3. BERT Etiket Kontrolü
    print("-" * 40)
    print("🧠 YAPAY ZEKA KARAR DAĞILIMI:")
    if 'BERT_Etiket' in df.columns:
        dagilim = df['BERT_Etiket'].value_counts()
        print(dagilim)
        
        # Oran Kontrolü
        olumlu_sayisi = dagilim.get('Olumlu', 0)
        olumsuz_sayisi = dagilim.get('Olumsuz', 0)
        
        if olumsuz_sayisi == 0:
            print("\n⚠️ DİKKAT: Hiç 'Olumsuz' yorum yok! Model şüpheli olabilir.")
        else:
            print(f"\n✅ Denge Kontrolü: {olumlu_sayisi} Olumlu / {olumsuz_sayisi} Olumsuz tespit edilmiş.")
    else:
        print("❌ HATA: 'BERT_Etiket' sütunu bulunamadı! Analiz yapılmamış olabilir.")

    # 4. Boş Değer Kontrolü
    bos_sayisi = df['Yorum'].isnull().sum()
    if bos_sayisi > 0:
        print(f"\n⚠️ UYARI: {bos_sayisi} adet boş yorum satırı var.")
    else:
        print("\n✅ Temizlik Kontrolü: Hiç boş satır yok.")

    print("-" * 40)
    print("🎉 KONTROL TAMAMLANDI.")

if __name__ == "__main__":
    check_up_yap()