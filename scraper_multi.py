import googleapiclient.discovery
import pandas as pd
from tqdm import tqdm # Progress bar kütüphanesi
import time

# --- AYARLAR ---
API_KEY = "AIzaSyB55_yJvLozPoOiqinvnmhDvO8OvjC0gEk" 

# ⚠️ ÖDEV: AŞAĞIDAKİ VİDEO ID'LERİNİ GERÇEK LİNKLERLE DOLDUR!
# Olumsuz yorumu bol olan videolar bulmaya çalış (Dengelemek için)
URUN_LISTESI = [
#    {"urun": "iPhone 15", "id": "yNNynS4cO44"},
#    {"urun": "Samsung S24", "id": "4whpgmmLDmg"},
#    {"urun": "MacBook Air", "id": "b-VsC5eqmqE"},
#    {"urun": "AirPods Pro", "id": "TQ5FRkvJTCQ"},
#    {"urun": "Dyson Supurge", "id": "O5V9s2Nxm04"} 
    {"urun": "Robot Supurge", "id": "dMBi5b-7J6Y"}, 
    {"urun": "Airfryer",      "id": "nObqMHpIVco"},
    {"urun": "PlayStation 5", "id": "BJJ0YyjdIvM"},
    {"urun": "Akilli Saat",   "id": "o_EhWt4uIMQ"}
        
]

def yorumlari_getir(video_id, urun_adi, youtube_client):
    yorumlar = []
    try:
        request = youtube_client.commentThreads().list(
            part="snippet", videoId=video_id, maxResults=100, textFormat="plainText"
        )
        
        while request:
            response = request.execute()
            for item in response['items']:
                detay = item['snippet']['topLevelComment']['snippet']
                yorumlar.append({
                    'Urun': urun_adi,
                    'Kaynak': 'YouTube', # Kaynak belirtiyoruz
                    'Yazar': detay['authorDisplayName'],
                    'Yorum': detay['textDisplay'],
                    'Begeni': detay['likeCount'],
                    'Tarih': detay['publishedAt']
                })
            
            # Sayfalama (Pagination)
            if 'nextPageToken' in response:
                request = youtube_client.commentThreads().list(
                    part="snippet", videoId=video_id, pageToken=response['nextPageToken'],
                    maxResults=100, textFormat="plainText"
                )
            else:
                break
                
    except Exception as e:
        print(f"⚠️ Hata ({urun_adi}): {e}")
        
    return yorumlar

def main():
    print("🏭 ÇOKLU ÜRÜN VERİ ÇEKME MODÜLÜ BAŞLATILIYOR...")
    
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    
    master_liste = []
    
    # TQDM ile havalı bir ilerleme çubuğu yapıyoruz
    for urun in tqdm(URUN_LISTESI, desc="Ürünler Taranıyor"):
        print(f"\n📡 {urun['urun']} için veri çekiliyor...")
        
        veriler = yorumlari_getir(urun['id'], urun['urun'], youtube)
        master_liste.extend(veriler) # Ana listeye ekle
        
        # Her ürünü ayrı ayrı da kaydet (Yedek olsun)
        df_gecici = pd.DataFrame(veriler)
        dosya_adi = f"yorumlar_{urun['urun'].replace(' ', '_')}.xlsx"
        df_gecici.to_excel(dosya_adi, index=False)
        print(f"   ✅ {urun['urun']}: {len(veriler)} yorum çekildi -> {dosya_adi}")
        
        time.sleep(1) # API'yi boğmamak için 1 saniye bekle

    # SONUÇ: BÜYÜK BİRLEŞTİRİLMİŞ DOSYA
    print("\n💾 TÜM VERİLER BİRLEŞTİRİLİYOR...")
    df_master = pd.DataFrame(master_liste)
    df_master.to_excel("yeni_veriler.xlsx", index=False)
    
    print(f"🎉 İŞLEM TAMAM! Toplam {len(df_master)} satır veri 'tum_urunler_master.xlsx' ve 'yeni_veriler.xlsx' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()