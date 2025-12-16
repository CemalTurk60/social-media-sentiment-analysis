import pandas as pd
import re
import string
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# --- AYARLAR ---
EXCEL_DOSYA_ADI = "sosyal_medya_full_data.xlsx" # Elindeki ana veri dosyası
KAYIT_DOSYASI_PKL = "tfidf_vectorizer.pkl"     # Eğitilmiş vektörleştiriciyi saklayacağız
TEMIZ_VERI_CSV = "ml_hazir_veri.csv"           # Temizlenmiş veriyi buraya kaydedeceğiz

# --- TÜRKÇE STOP WORDS ---
STOP_WORDS = {
    "ve", "ile", "bir", "bu", "şu", "o", "için", "da", "de", "ki", "mi", 
    "mu", "ama", "fakat", "lakin", "ancak", "yine", "böyle", "şöyle", 
    "diye", "bana", "sana", "ben", "sen", "biz", "siz", "onlar", "var", 
    "yok", "çok", "daha", "kadar", "gibi", "en", "mı", "mu", "mü", "şey"
}

# --- BASİT KÖK BULUCU (Stemmer) ---
# Türkçe NLP kütüphaneleri (Zemberek) kurulumu zor olduğu için 
# proje kapsamında basit bir kural tabanlı kök bulucu kullanıyoruz.
def basit_kok_bul(kelime):
    ekler = ["lar", "ler", "nın", "nin", "dan", "den", "mı", "mi", "un", "ün", "im", "sin", "siniz"]
    for ek in ekler:
        if kelime.endswith(ek) and len(kelime) > len(ek) + 2: # Köke zarar vermemek için kontrol
            return kelime[:-len(ek)]
    return kelime

def metin_temizle(metin):
    """
    Ham metni alır, ML için tertemiz hale getirir.
    """
    try:
        metin = str(metin).lower() # Küçük harf
        
        # 1. Regex Temizliği
        metin = re.sub(r'http\S+', '', metin) # Linkleri sil
        metin = re.sub(r'<.*?>', '', metin)   # HTML etiketlerini sil
        metin = re.sub(r'\d+', '', metin)     # Sayıları sil
        metin = re.sub(r'[^\w\s]', '', metin) # Noktalama işaretlerini sil (Emoji dahil)
        
        # 2. Kelime İşlemleri
        kelimeler = metin.split()
        
        # Stop Words Temizliği ve Kök Bulma
        temiz_kelimeler = [
            basit_kok_bul(kelime) for kelime in kelimeler 
            if kelime not in STOP_WORDS and len(kelime) > 2
        ]
        
        return " ".join(temiz_kelimeler)
        
    except:
        return ""

def veri_hazirla():
    print("🔄 Veri Ön İşleme (Preprocessing) Başlıyor...")
    
    # 1. Veriyi Oku
    df = pd.read_excel(EXCEL_DOSYA_ADI)
    print(f"✅ {len(df)} satır ham veri okundu.")
    
    # 2. Temizlik Yap
    print("🧼 Metinler temizleniyor (Regex + Stemming)...")
    df['Temiz_Yorum'] = df['Yorum'].apply(metin_temizle)
    
    # Boş kalan satırları at (Temizlik sonrası boşalanlar)
    df = df[df['Temiz_Yorum'].str.len() > 2]
    print(f"✅ Temizlik sonrası kalan veri: {len(df)} satır.")
    
    # 3. Etiketleme (Labeling) - ŞİMDİLİK GEÇİCİ
    # ML modelini eğitmek için elimizde "Doğru Cevaplar" (Etiketler) olması lazım.
    # Şimdilik kendi yazdığımız sözlük tabanlı analiz sonucunu "Doğru Cevap" kabul edeceğiz.
    # (İdeal dünyada elle etiketlemek gerekirdi ama zamanımız yok).
    
    from proje_v2 import TezAnalizSistemi # Önceki kodumuzdan sınıfı çağırıyoruz
    analiz_sistemi = TezAnalizSistemi(EXCEL_DOSYA_ADI)
    df[['Skor', 'Etiket']] = df['Yorum'].apply(analiz_sistemi.sentiment_hesapla)
    
    # Sadece Olumlu/Olumsuz olanları al (Nötr'ü at, ML kafası karışmasın)
    df_egitim = df[df['Etiket'] != 'Nötr'].copy()
    
    # Etiketleri Sayıya Çevir (Olumlu=1, Olumsuz=0)
    df_egitim['Hedef'] = df_egitim['Etiket'].apply(lambda x: 1 if x == 'Olumlu' else 0)
    
    print(f"🤖 Eğitim için kullanılacak veri sayısı: {len(df_egitim)} (Nötrler çıkarıldı)")
    
    # 4. CSV Olarak Kaydet (Model bu dosyayı kullanacak)
    df_egitim.to_csv(TEMIZ_VERI_CSV, index=False)
    print(f"💾 Hazır veri kaydedildi: {TEMIZ_VERI_CSV}")

    return df_egitim

if __name__ == "__main__":
    veri_hazirla()