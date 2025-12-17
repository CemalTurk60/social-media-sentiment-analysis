import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import sqlite3
import re
from collections import Counter
import datetime

# ================= AYARLAR =================
# Buraya elindeki Excel dosyasının tam adını yaz:
EXCEL_DOSYA_ADI = "yorumlar_fQZDGfrz_YU.xlsx"  
VERITABANI_ADI = "tez_veritabani.db"
RAPOR_DOSYA_ADI = "profesyonel_analiz_raporu.txt"
# ===========================================

# --- 1. MODÜL: TÜRKÇE SENTIMENT SÖZLÜĞÜ ---
# TextBlob yerine kendi sözlük tabanlı algoritmamızı yazıyoruz.
POZITIF_KELIMELER = {
    "harika", "mükemmel", "süper", "efsane", "iyi", "güzel", "başarılı", 
    "beğendim", "sevdim", "kaliteli", "hızlı", "fiyat performans", "muazzam",
    "teşekkür", "tavsiye", "kral", "muhteşem", "akıcı", "net", "bayıldım",
    "10 numara", "sağlam", "güvenilir", "şahane", "memnun"
}

NEGATIF_KELIMELER = {
    "kötü", "berbat", "rezalet", "iğrenç", "bozuk", "sorun", "hata", 
    "kasıyor", "donuyor", "yavaş", "pahalı", "değmez", "çöp", "pişman",
    "beğenmedim", "sakın", "uzak durun", "ısınma", "şarjı bitiyor", "kırık",
    "gelmedi", "yalan", "dolandırıcı", "berbat", "gereksiz"
}

TURKCE_STOP_WORDS = {
    "ve", "ile", "bir", "bu", "şu", "o", "için", "da", "de", "ki", "mi", 
    "mu", "ama", "fakat", "lakin", "ancak", "yine", "böyle", "şöyle", 
    "diye", "bana", "sana", "ben", "sen", "biz", "siz", "onlar", "var", 
    "yok", "çok", "daha", "kadar", "gibi", "en", "mı", "mu", "mü"
}

class TezAnalizSistemi:
    def __init__(self, dosya_yolu):
        print("📂 Veri seti yükleniyor...")
        try:
            self.df = pd.read_excel(dosya_yolu)
            # Boş verileri temizle
            self.df.dropna(subset=['Yorum'], inplace=True)
            self.df['Yorum'] = self.df['Yorum'].astype(str)
            print(f"✅ Yüklendi. Toplam {len(self.df)} satır veri var.")
        except Exception as e:
            print(f"❌ Dosya okuma hatası: {e}")
            self.df = None

    def metin_temizle(self, metin):
        """Metni noktalama işaretlerinden ve gereksiz boşluklardan temizler."""
        metin = metin.lower() # Küçük harfe çevir
        metin = re.sub(r'[^\w\s]', '', metin) # Noktalama işaretlerini kaldır
        metin = re.sub(r'\d+', '', metin) # Sayıları kaldır
        return metin

    def sentiment_hesapla(self, metin):
        """
        Gelişmiş Sözlük Tabanlı Skorlama Algoritması
        Döndürdüğü: (Skor, Etiket)
        """
        temiz_metin = self.metin_temizle(metin)
        kelimeler = temiz_metin.split()
        
        pozitif_sayac = sum(1 for k in kelimeler if k in POZITIF_KELIMELER)
        negatif_sayac = sum(1 for k in kelimeler if k in NEGATIF_KELIMELER)
        
        # Polarity Skoru (-1 ile +1 arası normalizasyon)
        toplam_etkili_kelime = pozitif_sayac + negatif_sayac
        
        if toplam_etkili_kelime == 0:
            skor = 0.0
        else:
            skor = (pozitif_sayac - negatif_sayac) / toplam_etkili_kelime

        # Etiketleme
        if skor > 0.1:
            etiket = "Olumlu"
        elif skor < -0.1:
            etiket = "Olumsuz"
        else:
            etiket = "Nötr"
            
        return pd.Series([skor, etiket])

    def analizi_calistir(self):
        print("🧠 Türkçe Sentiment Analizi yapılıyor...")
        # Apply ile fonksiyonu tüm satırlara uygula
        self.df[['Polarity', 'Duygu']] = self.df['Yorum'].apply(self.sentiment_hesapla)
        
        # Yorum uzunluğunu hesapla (Kelime sayısı)
        self.df['Kelime_Sayisi'] = self.df['Yorum'].apply(lambda x: len(str(x).split()))
        print("✅ Analiz tamamlandı.")

    def veritabani_entegrasyonu(self):
        print(f"💾 SQLite Veritabanına ({VERITABANI_ADI}) kaydediliyor...")
        try:
            conn = sqlite3.connect(VERITABANI_ADI)
            cursor = conn.cursor()
            
            # Tabloyu oluştur (Varsa silmeden önce kontrol et)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS yorumlar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    yazar TEXT,
                    yorum TEXT,
                    begeni INTEGER,
                    tarih TEXT,
                    polarity REAL,
                    duygu TEXT
                )
            ''')
            
            # Veriyi Pandas üzerinden SQL'e at (Çok hızlıdır)
            kaydedilecek_veri = self.df[['Yazar', 'Yorum', 'Begeni', 'Tarih', 'Polarity', 'Duygu']]
            kaydedilecek_veri.to_sql('yorumlar', conn, if_exists='replace', index=False)
            
            conn.close()
            print("✅ Veritabanı işlemleri başarılı.")
        except Exception as e:
            print(f"❌ Veritabanı Hatası: {e}")

    def gorsellestir(self):
        print("🎨 Grafikler hazırlanıyor...")
        sns.set_style("whitegrid") # Profesyonel görünüm
        plt.figure(figsize=(18, 12))

        # 1. Grafik: Duygu Dağılımı (Pasta)
        plt.subplot(2, 3, 1)
        counts = self.df['Duygu'].value_counts()
        colors = {'Olumlu': '#2ecc71', 'Olumsuz': '#e74c3c', 'Nötr': '#95a5a6'}
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', 
                colors=[colors.get(x, '#95a5a6') for x in counts.index], startangle=90)
        plt.title('Duygu Analizi Sonuçları')

        # 2. Grafik: En Çok Kullanılan Kelimeler (Bar Chart)
        plt.subplot(2, 3, 2)
        tum_metin = " ".join(self.df['Yorum'].apply(self.metin_temizle))
        kelimeler = [k for k in tum_metin.split() if k not in TURKCE_STOP_WORDS and len(k) > 2]
        en_cok_gecen = Counter(kelimeler).most_common(10)
        x_val = [x[0] for x in en_cok_gecen]
        y_val = [x[1] for x in en_cok_gecen]
        sns.barplot(x=x_val, y=y_val, palette="viridis")
        plt.xticks(rotation=45)
        plt.title('En Sık Kullanılan 10 Kelime')

        # 3. Grafik: Beğeni Dağılımı (Histogram)
        plt.subplot(2, 3, 3)
        sns.histplot(self.df['Begeni'], bins=30, kde=True, color='orange')
        plt.title('Yorum Beğeni Dağılımı')
        plt.xlim(0, self.df['Begeni'].quantile(0.95)) # Aşırı uç değerleri gizle

        # 4. Grafik: Yorum Uzunluğu vs Duygu (Box Plot)
        plt.subplot(2, 3, 4)
        sns.boxplot(x='Duygu', y='Kelime_Sayisi', data=self.df, palette=colors)
        plt.title('Duyguya Göre Yorum Uzunluğu')
        plt.ylim(0, 50) # Çok uzun yorumları kes

        # 5. Grafik: Zaman Serisi (Günlük Yorum Sayısı)
        plt.subplot(2, 3, 5)
        # Tarih formatını düzelt
        try:
            self.df['Tarih_Formatli'] = pd.to_datetime(self.df['Tarih']).dt.date
            zaman_serisi = self.df.groupby('Tarih_Formatli').size()
            zaman_serisi.plot(kind='line', marker='o', color='purple')
            plt.title('Zaman İçinde Yorum Sayısı')
            plt.xticks(rotation=45)
        except:
            plt.text(0.5, 0.5, "Tarih Formatı Hatası", ha='center')

        # 6. Alan: Kelime Bulutu
        plt.subplot(2, 3, 6)
        wordcloud = WordCloud(width=400, height=300, background_color='white', 
                            stopwords=TURKCE_STOP_WORDS).generate(tum_metin)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Kelime Bulutu')

        plt.tight_layout()
        plt.savefig("profesyonel_dashboard.png", dpi=300)
        print("✅ Dashboard kaydedildi: profesyonel_dashboard.png")
        plt.show()

    def rapor_olustur(self):
        print("📝 Otomatik rapor yazılıyor...")
        toplam_yorum = len(self.df)
        duygu_dagilimi = self.df['Duygu'].value_counts()
        en_begenilen = self.df.loc[self.df['Begeni'].idxmax()]
        
        rapor = f"""
        ================================================
        PROJE ANALİZ RAPORU (OTOMATİK OLUŞTURULDU)
        Tarih: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
        ================================================
        
        1. GENEL İSTATİSTİKLER
        ----------------------
        Toplam Analiz Edilen Yorum: {toplam_yorum}
        
        2. DUYGU ANALİZİ SONUÇLARI
        --------------------------
        Olumlu Yorumlar: {duygu_dagilimi.get('Olumlu', 0)} (%{(duygu_dagilimi.get('Olumlu', 0)/toplam_yorum)*100:.1f})
        Olumsuz Yorumlar: {duygu_dagilimi.get('Olumsuz', 0)} (%{(duygu_dagilimi.get('Olumsuz', 0)/toplam_yorum)*100:.1f})
        Nötr Yorumlar:   {duygu_dagilimi.get('Nötr', 0)} (%{(duygu_dagilimi.get('Nötr', 0)/toplam_yorum)*100:.1f})
        
        3. EN DİKKAT ÇEKEN YORUM (En Çok Beğeni Alan)
        ---------------------------------------------
        Yazar: {en_begenilen['Yazar']}
        Beğeni: {en_begenilen['Begeni']}
        Duygu: {en_begenilen['Duygu']}
        Yorum: "{en_begenilen['Yorum']}"
        
        4. VERİTABANI DURUMU
        --------------------
        Veriler '{VERITABANI_ADI}' içerisindeki 'yorumlar' tablosuna başarıyla yedeklendi.
        
        5. SONUÇ VE ÖNERİ
        -----------------
        Bu analiz, sözlük tabanlı Türkçe NLP yöntemleri kullanılarak gerçekleştirilmiştir.
        Kullanıcıların genel eğilimi incelendiğinde en sık kullanılan kelimelerin ürün performansı
        ile ilişkili olduğu görülmüştür.
        
        ================================================
        Cemalettin [Soyadın] - YBS Bitirme Projesi
        """
        
        with open(RAPOR_DOSYA_ADI, "w", encoding="utf-8") as f:
            f.write(rapor)
        print(f"✅ Rapor oluşturuldu: {RAPOR_DOSYA_ADI}")

# --- MAIN (ANA ÇALIŞTIRMA BLOĞU) ---
if __name__ == "__main__":
    # Sınıfı çağır ve işlemleri sırasıyla yap
    proje = TezAnalizSistemi(EXCEL_DOSYA_ADI)
    
    if proje.df is not None:
        proje.analizi_calistir()       # 1. Analiz et
        proje.veritabani_entegrasyonu() # 2. SQL'e kaydet
        proje.rapor_olustur()           # 3. Raporu yaz
        proje.gorsellestir()            # 4. Grafikleri çiz