# --- YOUTUBE YORUM ÇEKME BOTU (v1.0) ---
import googleapiclient.discovery
import pandas as pd
import sys

# ================= AYARLAR =================
# 1. Google'dan aldığın uzun şifreyi tırnak içine yapıştır:
API_KEY = "AIzaSyB55_yJvLozPoOiqinvnmhDvO8OvjC0gEk" 

# 2. Videonun ID'sini tırnak içine yapıştır:
# Örnek Link: youtube.com/watch?v=dQw4w9WgXcQ -> ID: dQw4w9WgXcQ
VIDEO_ID = "fQZDGfrz_YU" 
# ===========================================

def main():
    print(f"📡 YouTube'a bağlanılıyor... (Video ID: {VIDEO_ID})")

    try:
        # API İstemcisini oluşturuyoruz
        youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=API_KEY)

        yorumlar = []
        video_response = youtube.commentThreads().list(
            part="snippet",
            videoId=VIDEO_ID,
            maxResults=100, # Her sayfada 100 yorum al
            textFormat="plainText"
        )

        sayfa_sayisi = 1
        print("📥 Veri çekme işlemi başladı...")

        # Sayfalama Döngüsü (Pagination)
        while video_response:
            response = video_response.execute()

            for item in response['items']:
                # Gelen paketin içinden gerekli bilgileri cımbızlıyoruz
                yorum_detay = item['snippet']['topLevelComment']['snippet']
                
                veri = {
                    'Yazar': yorum_detay['authorDisplayName'],
                    'Yorum': yorum_detay['textDisplay'],
                    'Begeni': yorum_detay['likeCount'],
                    'Tarih': yorum_detay['publishedAt']
                }
                yorumlar.append(veri)

            # İlerleme durumunu ekrana yaz
            print(f"✅ Sayfa {sayfa_sayisi} işlendi. (Toplam {len(yorumlar)} yorum)")

            # Sonraki sayfa var mı? Varsa döngü devam eder.
            if 'nextPageToken' in response:
                video_response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=VIDEO_ID,
                    pageToken=response['nextPageToken'],
                    maxResults=100,
                    textFormat="plainText"
                )
                sayfa_sayisi += 1
            else:
                break # Başka sayfa yoksa çık

        # Veriyi Excel'e Kaydetme
        print("💾 Veriler Excel'e dönüştürülüyor...")
        df = pd.DataFrame(yorumlar)
        
        # Dosya ismi video ID ile başlasın ki karışmasın
        dosya_ismi = f"yorumlar_{VIDEO_ID}.xlsx"
        df.to_excel(dosya_ismi, index=False)
        
        print(f"\n🎉 İŞLEM BAŞARILI! Dosya oluşturuldu: {dosya_ismi}")
        print(f"📊 Toplam {len(df)} satır veri çekildi.")

    except Exception as e:
        print(f"\n❌ BİR HATA OLUŞTU:")
        print(e)
        print("⚠️ İPUCU: API Key'i veya Video ID'yi doğru yazdığından emin ol.")

if __name__ == "__main__":
    main()