import streamlit as st
import pandas as pd
import plotly.express as px

# --- AYARLAR ---
st.set_page_config(page_title="Tez Analiz Paneli", layout="wide")

# --- BAŞLIK VE GİRİŞ ---
st.title("📱 Ürün Yorumları Duygu Analizi Projesi")
st.markdown("""
Bu proje, **iPhone, Samsung, Dyson** gibi ürünlere gelen binlerce yorumu 
**Yapay Zeka (BERT)** ile analiz ederek müşteri memnuniyetini ölçer.
""")

# --- VERİYİ YÜKLE ---
@st.cache_data # Performans için veriyi hafızada tutar
def veri_yukle():
    # Excel dosyasını okuyoruz
    df = pd.read_excel("bert_analiz_sonuclari.xlsx")
    return df

try:
    df = veri_yukle()
    st.success(f"✅ Analiz Sonuçları Yüklendi! Toplam {len(df)} veri inceleniyor.")
except FileNotFoundError:
    st.error("❌ HATA: 'bert_analiz_sonuclari.xlsx' dosyası bulunamadı! Lütfen önce analizi çalıştırın.")
    st.stop()

# --- SOL MENÜ (SIDEBAR) ---
st.sidebar.header("🔍 Filtrele")
secilen_urun = st.sidebar.selectbox("Hangi Ürünü İncelemek İstersin?", df["Urun"].unique())

# Filtreleme İşlemi
filtrelenmis_veri = df[df["Urun"] == secilen_urun]

# --- ANA İSTATİSTİKLER (KPI) ---
col1, col2, col3 = st.columns(3)

toplam_yorum = len(filtrelenmis_veri)
olumlu_sayisi = len(filtrelenmis_veri[filtrelenmis_veri["BERT_Etiket"] == "Olumlu"])
olumsuz_sayisi = len(filtrelenmis_veri[filtrelenmis_veri["BERT_Etiket"] == "Olumsuz"])

col1.metric("Toplam Yorum", toplam_yorum)
col2.metric("🟢 Olumlu Yorumlar", olumlu_sayisi)
col3.metric("🔴 Olumsuz Yorumlar", olumsuz_sayisi)

# --- GRAFİKLER ---
col_grafik1, col_grafik2 = st.columns(2)

with col_grafik1:
    st.subheader(f"{secilen_urun} Duygu Dağılımı")
    fig_pasta = px.pie(filtrelenmis_veri, names="BERT_Etiket", 
                       title="Olumlu vs Olumsuz Oranı",
                       color="BERT_Etiket",
                       color_discrete_map={"Olumlu": "green", "Olumsuz": "red"})
    st.plotly_chart(fig_pasta, use_container_width=True)

with col_grafik2:
    st.subheader("Güven Skoru Dağılımı")
    fig_hist = px.histogram(filtrelenmis_veri, x="BERT_Guven_Skoru", 
                            nbins=20, title="Yapay Zeka Ne Kadar Emin?",
                            color_discrete_sequence=["blue"])
    st.plotly_chart(fig_hist, use_container_width=True)

# --- VERİ TABLOSU ---
st.subheader("📝 Detaylı Yorum Listesi")
st.dataframe(filtrelenmis_veri[["Yorum", "BERT_Etiket", "BERT_Guven_Skoru"]])