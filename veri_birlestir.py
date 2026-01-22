import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

# --- ÇALIŞMA DİZİNİ AYARI ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"📂 Çalışma Dizini: {os.getcwd()}")

# --- AYARLAR ---
DOSYA_OGRETMEN = "bert_analiz_sonuclari.xlsx"
DOSYA_OGRENCI  = "yeni_veriler.xlsx"
DOSYA_KAGGLE   = "ham_veriler/eticaret_urun_yorumlari.csv"
HEDEF_TOPLAM   = 10000

print("\n🚀 FİNAL BİRLEŞTİRME VE ETİKETLEME OPERASYONU (V4 - TÜRKÇE LABEL DESTEKLİ)...\n")

def sutunlari_duzelt(df, kaynak_adi):
    """Sütun isimlerini otomatik bulup standart hale getirir."""
    df.columns = [str(c).lower().strip() for c in df.columns]
    
    # Yorum sütunu bul
    olasi_yorum = ['yorum', 'metin', 'text', 'review', 'comment', 'içerik', 'body']
    for ad in olasi_yorum:
        for col in df.columns:
            if ad in col:
                df = df.rename(columns={col: 'yorum'})
                break
    
    # Duygu sütunu bul
    olasi_duygu = ['duygu', 'durum', 'label', 'sentiment', 'score', 'puan', 'etiket', 'bert_etiket']
    for ad in olasi_duygu:
        for col in df.columns:
            if ad in col:
                df = df.rename(columns={col: 'duygu'})
                break
    return df

def etiketleri_standartlastir(df):
    """Etiketleri (Olumlu, 1, Positive) -> (Pozitif, Negatif, Nötr) yapar."""
    if 'duygu' not in df.columns: return df
    
    # Debug: Ne var ne yok görelim
    print(f"   ℹ️ Gelen Etiketler: {df['duygu'].unique()[:5]}") 
    
    def cevir(x):
        s = str(x).lower().strip()
        # Pozitif Tanımları
        if s in ['1', '1.0', 'pozitif', 'positive', 'label_1', 'pos', 'olumlu']: return "Pozitif"
        # Negatif Tanımları
        if s in ['0', '0.0', 'negatif', 'negative', 'label_0', 'neg', 'olumsuz']: return "Negatif"
        # Nötr Tanımları
        if s in ['2', '2.0', 'nötr', 'notr', 'neutral', 'label_2', 'neu']: return "Nötr"
        
        return "Nötr" # Tanınmayanlar
        
    df['duygu'] = df['duygu'].apply(cevir)
    return df

# 1. ADIM: ÖĞRETMEN VERİYİ YÜKLE
print(f"1. Öğretmen veri okunuyor: {DOSYA_OGRETMEN}")
df_ogretmen = pd.DataFrame()
if os.path.exists(DOSYA_OGRETMEN):
    try:
        df_ogretmen = pd.read_excel(DOSYA_OGRETMEN)
        df_ogretmen = sutunlari_duzelt(df_ogretmen, "Öğretmen")
        
        if 'yorum' in df_ogretmen.columns and 'duygu' in df_ogretmen.columns:
            df_ogretmen = df_ogretmen[['yorum', 'duygu']].dropna()
            df_ogretmen = etiketleri_standartlastir(df_ogretmen) # ETİKETLERİ DÜZELT
            print(f"   ✅ Hazır! {len(df_ogretmen)} satır eğitim verisi.")
        else:
            print("   ⚠️ Sütunlar eksik.")
    except Exception as e:
        print(f"   ❌ Hata: {e}")

# 2. ADIM: ÖĞRENCİ VERİYİ YÜKLE
print(f"\n2. Öğrenci veri okunuyor: {DOSYA_OGRENCI}")
df_ogrenci = pd.DataFrame()
if os.path.exists(DOSYA_OGRENCI):
    try:
        df_ogrenci = pd.read_excel(DOSYA_OGRENCI)
        df_ogrenci = sutunlari_duzelt(df_ogrenci, "Öğrenci")
        if 'yorum' in df_ogrenci.columns:
            df_ogrenci = df_ogrenci[['yorum']].dropna()
            print(f"   ✅ Hazır! {len(df_ogrenci)} satır.")
    except Exception as e: print(f"Hata: {e}")

# 3. ADIM: KAGGLE VERİSİNİ YÜKLE
print(f"\n3. Kaggle dosyası yükleniyor: {DOSYA_KAGGLE}")
df_kaggle = pd.DataFrame()
if os.path.exists(DOSYA_KAGGLE):
    try:
        # Önce noktalı virgül dene
        df_kaggle = pd.read_csv(DOSYA_KAGGLE, sep=';', encoding='utf-8')
        df_kaggle = sutunlari_duzelt(df_kaggle, "Kaggle")
        
        # Sütunlar gelmediyse virgülle dene
        if 'yorum' not in df_kaggle.columns:
            df_kaggle = pd.read_csv(DOSYA_KAGGLE, sep=',', encoding='utf-8')
            df_kaggle = sutunlari_duzelt(df_kaggle, "Kaggle (Virgül)")

        if 'yorum' in df_kaggle.columns and 'duygu' in df_kaggle.columns:
            df_kaggle = df_kaggle[['yorum', 'duygu']].dropna()
            df_kaggle = etiketleri_standartlastir(df_kaggle) # ETİKETLERİ DÜZELT
            print(f"   ✅ Kaggle verisi hazır: {len(df_kaggle)} satır.")
        else:
             print("   ❌ Kaggle sütunları eşleştirilemedi.")
    except Exception as e:
        print(f"   ❌ Kaggle okuma hatası: {e}")

# 4. ADIM: AUTO-LABELING
# Eğer eski veri yoksa veya hepsi "Nötr" olduysa Kaggle'ı kullan
egitim_verisi = pd.DataFrame()
if not df_ogretmen.empty and len(df_ogretmen['duygu'].unique()) > 1:
    egitim_verisi = df_ogretmen
else:
    print("   ⚠️ Öğretmen verisi yetersiz (Tek sınıf), Kaggle kullanılıyor...")
    egitim_verisi = df_kaggle.sample(n=min(5000, len(df_kaggle)), random_state=42)

if not egitim_verisi.empty and not df_ogrenci.empty:
    print("\n🤖 YAPAY ZEKA MODELİ EĞİTİLİYOR...")
    print(f"   Eğitim sınıfları: {egitim_verisi['duygu'].unique()}") # Kontrol
    
    vec = TfidfVectorizer(max_features=5000)
    X_train = vec.fit_transform(egitim_verisi['yorum'].astype(str))
    
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, egitim_verisi['duygu'])
    
    print("   -> Yeni veriler etiketleniyor...")
    X_test = vec.transform(df_ogrenci['yorum'].astype(str))
    preds = model.predict(X_test)
    df_ogrenci['duygu'] = preds
    print(f"   ✅ TAHMİN BİTTİ!")
else:
    if not df_ogrenci.empty: df_ogrenci['duygu'] = 'Nötr'

# 5. ADIM: BİRLEŞTİRME
print("\n📦 Veriler birleştiriliyor...")
df_bizim = pd.concat([df_ogretmen, df_ogrenci], ignore_index=True)
print(f"   Bizim Topladığımız: {len(df_bizim)} adet")

eksik = HEDEF_TOPLAM - len(df_bizim)
if eksik > 0 and not df_kaggle.empty:
    print(f"   Hedef için Kaggle'dan {eksik} veri ekleniyor...")
    df_ek = df_kaggle.sample(n=min(eksik, len(df_kaggle)), random_state=123)
    df_final = pd.concat([df_bizim, df_ek], ignore_index=True)
else:
    df_final = df_bizim

# 6. ADIM: KAYIT
print("\n✂️ %70 Eğitim - %30 Test ayrımı yapılıyor...")
if len(df_final) > 0:
    print(f"   Toplam Veri: {len(df_final)}")
    print(f"   Etiket Dağılımı:\n{df_final['duygu'].value_counts()}")

    X_train, X_test, y_train, y_test = train_test_split(df_final['yorum'], df_final['duygu'], test_size=0.30, random_state=42)

    if not os.path.exists("ham_veriler"): os.makedirs("ham_veriler")
    
    pd.DataFrame({'yorum': X_train, 'duygu': y_train}).to_excel("ham_veriler/egitim_seti_70.xlsx", index=False)
    pd.DataFrame({'yorum': X_test, 'duygu': y_test}).to_excel("ham_veriler/test_seti_30.xlsx", index=False)

    print(f"\n✨ MUTLU SON! Dosyalar kaydedildi.")
else:
    print("❌ HATA: Veri seti boş kaldı!")