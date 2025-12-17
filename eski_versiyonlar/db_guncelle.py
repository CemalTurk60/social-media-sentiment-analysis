import pandas as pd
import sqlite3

# Dosyalar
EXCEL_DOSYASI = "bert_analiz_sonuclari.xlsx"
DB_DOSYASI = "tez_veritabani.db"

def veritabani_esitle():
    print("🔄 Veritabanı Eşitleme Başlıyor...")
    
    # 1. Excel'i Oku
    try:
        df = pd.read_excel(EXCEL_DOSYASI)
        print(f"✅ Excel Okundu: {len(df)} satır veri var.")
    except:
        print("❌ Excel dosyası bulunamadı!")
        return

    # 2. Veritabanına Bağlan
    conn = sqlite3.connect(DB_DOSYASI)
    cursor = conn.cursor()
    
    # Eski tabloyu temizle (Varsa)
    cursor.execute("DROP TABLE IF EXISTS yorumlar_analizli")
    
    # 3. Yeni Veriyi Kaydet
    # 'yorumlar_analizli' adında yeni bir tablo yaratıp içine basıyoruz
    df.to_sql("yorumlar_analizli", conn, if_exists="replace", index=False)
    
    conn.close()
    print(f"🎉 İŞLEM TAMAM! Veriler '{DB_DOSYASI}' içine yedeklendi.")
    print("Artık hem Excel'in hem Veritabanın güncel.")

if __name__ == "__main__":
    veritabani_esitle()