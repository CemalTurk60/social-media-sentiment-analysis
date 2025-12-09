import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- AYARLAR ---
# Buraya az önce oluşan dosyanın ismini TAM olarak yaz:
DOSYA_ADI = "yorumlar_fQZDGfrz_YU.xlsx" 

def duygu_analizi_yap(metin):
    """
    Bu fonksiyon şimdilik basit bir kural tabanlı analiz yapar.
    İleride burayı Yapay Zeka (BERT) ile değiştireceğiz.
    """
    try:
        # TextBlob İngilizce temellidir ama basit demo için iş görür.
        # Türkçe karakterleri bazen tanımaz, bu sadece MVP (Demo) içindir.
        analiz = TextBlob(str(metin))
        skor = analiz.sentiment.polarity
        
        if skor > 0:
            return 'Olumlu'
        elif skor < 0:
            return 'Olumsuz'
        else:
            return 'Nötr'
    except:
        return 'Nötr'

def main():
    print(f"📊 {DOSYA_ADI} dosyası okunuyor...")
    
    try:
        # 1. Excel dosyasını oku
        df = pd.read_excel(DOSYA_ADI)
        print("✅ Dosya başarıyla yüklendi.")
        
        # 2. Analiz Fonksiyonunu Uygula
        print("🧠 Duygu analizi yapılıyor (Bu işlem demo amaçlıdır)...")
        df['Duygu'] = df['Yorum'].apply(duygu_analizi_yap)
        
        # 3. Sonuçları Say
        sonuclar = df['Duygu'].value_counts()
        print("\n--- ANALİZ SONUÇLARI ---")
        print(sonuclar)
        
        # 4. Pasta Grafiği Çiz (Görselleştirme)
        plt.figure(figsize=(8, 8))
        plt.pie(sonuclar, labels=sonuclar.index, autopct='%1.1f%%', 
                colors=['#FF9999', '#66B2FF', '#99FF99'])
        plt.title(f'Ürün Yorumları Duygu Dağılımı\n(Toplam {len(df)} Yorum)')
        
        # 5. Grafiği Kaydet
        resim_adi = "analiz_grafigi.png"
        plt.savefig(resim_adi)
        print(f"\n📈 Grafik çizildi ve kaydedildi: {resim_adi}")
        
        # Grafiği Ekranda Göster
        plt.show()

    except FileNotFoundError:
        print("❌ HATA: Dosya bulunamadı! Lütfen dosya adını doğru yazdığından emin ol.")
    except Exception as e:
        print(f"❌ BEKLENMEYEN HATA: {e}")

if __name__ == "__main__":
    main()