import pandas as pd
import random
import time

# --- AYARLAR ---
GIRIS_DOSYASI = "tum_urunler_master.xlsx" # Scraper'dan çıkan master dosya
CIKIS_DOSYASI = "sosyal_medya_full_data.xlsx"

# Gerçekçilik için Hashtag ve Mention Havuzu
HASHTAGS = ["#teknoloji", "#inceleme", "#unboxing", "#fiyatperformans", "#tech", "#alisveris"]
MENTIONS = ["@AppleDestek", "@SamsungTurkiye", "@TeknoMarket", "@Webtekno", "@ShiftDelete"]

def instagram_simule_et(row):
    """YouTube yorumunu al, Instagram tarzına çevir (Bol emoji, kısa)"""
    yorum = str(row['Yorum'])
    
    # Instagram yorumları genelde daha kısadır
    if len(yorum) > 100:
        yorum = yorum[:97] + "..."
        
    emojiler = ["🔥", "😍", "❤️", "👏", "🙌", "💸", "🤔", "💩", "😡"]
    secilen_emoji = random.choice(emojiler)
    secilen_tag = random.choice(HASHTAGS)
    
    yeni_yorum = f"{secilen_emoji} {yorum} {secilen_tag}"
    
    return {
        'Urun': row['Urun'],
        'Kaynak': 'Instagram (Simulated)', # Şeffaflık önemli!
        'Yazar': f"insta_user_{random.randint(1000,9999)}",
        'Yorum': yeni_yorum,
        'Begeni': random.randint(5, 500), # Instagram'da beğeni boldur
        'Tarih': row['Tarih']
    }

def twitter_simule_et(row):
    """YouTube yorumunu al, Twitter tarzına çevir (Mention, agresif/net)"""
    yorum = str(row['Yorum'])
    
    # Twitter 280 karakter sınırı
    if len(yorum) > 280:
        yorum = yorum[:277] + "..."
    
    secilen_mention = random.choice(MENTIONS) if random.random() > 0.7 else ""
    
    yeni_yorum = f"{secilen_mention} {yorum}"
    
    return {
        'Urun': row['Urun'],
        'Kaynak': 'Twitter (Simulated)',
        'Yazar': f"@user_{random.randint(10000,99999)}",
        'Yorum': yeni_yorum,
        'Begeni': random.randint(0, 100),
        'Tarih': row['Tarih']
    }

def main():
    print("🎭 SOSYAL MEDYA SİMÜLASYON MOTORU BAŞLATILIYOR...")
    
    try:
        df_youtube = pd.read_excel(GIRIS_DOSYASI)
        print(f"✅ Kaynak Veri: {len(df_youtube)} YouTube yorumu yüklendi.")
    except:
        print(f"❌ HATA: Önce '{GIRIS_DOSYASI}' dosyasını oluşturmalısın (scraper_multi.py çalıştır)!")
        return

    simule_veriler = []
    
    print("🔄 Veriler türetiliyor...")
    # Verinin %40'ı kadar Instagram, %40'ı kadar Twitter verisi üretelim
    orneklem = df_youtube.sample(frac=0.8, replace=True) 
    
    for index, row in orneklem.iterrows():
        # Yazı tura at: Yarısı Insta, Yarısı Twitter
        if random.random() > 0.5:
            simule_veriler.append(instagram_simule_et(row))
        else:
            simule_veriler.append(twitter_simule_et(row))
            
    df_simule = pd.DataFrame(simule_veriler)
    
    # YouTube verisi ile Simüle veriyi birleştir
    df_final = pd.concat([df_youtube, df_simule], ignore_index=True)
    
    # Karıştır (Shuffle)
    df_final = df_final.sample(frac=1).reset_index(drop=True)
    
    print(f"📊 YouTube Verisi: {len(df_youtube)}")
    print(f"📊 Üretilen Simülasyon: {len(df_simule)}")
    print(f"📈 TOPLAM VERİ SETİ: {len(df_final)}")
    
    df_final.to_excel(CIKIS_DOSYASI, index=False)
    print(f"💾 BÜYÜK FİNAL DOSYASI KAYDEDİLDİ: {CIKIS_DOSYASI}")

if __name__ == "__main__":
    main()