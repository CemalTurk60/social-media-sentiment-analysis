import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import torch

# --- AYARLAR ---
GIRIS_DOSYASI = "sosyal_medya_full_data.xlsx"
CIKIS_DOSYASI = "bert_analiz_sonuclari.xlsx"
# Hazır eğitilmiş profesyonel Türkçe model:
MODEL_ADI = "savasy/bert-base-turkish-sentiment-cased" 

def bert_ile_analiz_et():
    print("🧠 BERT Modeli Yükleniyor... (Bu işlem ilk seferde model indireceği için biraz sürebilir)")
    
    # Cihaz seçimi (Ekran kartı varsa GPU, yoksa CPU)
    cihaz = 0 if torch.cuda.is_available() else -1
    if cihaz == 0:
        print("🚀 GPU Tespit Edildi! Analiz Ferrari hızında olacak.")
    else:
        print("🐢 GPU Bulunamadı, CPU kullanılıyor. Biraz yavaş olabilir, sabret.")

    # Modeli huggingface'den çekiyoruz
    # sentiment-analysis pipeline'ı işimizi çok kolaylaştırır
    analizci = pipeline("sentiment-analysis", model=MODEL_ADI, tokenizer=MODEL_ADI, device=cihaz)
    
    print("📂 Veri Yükleniyor...")
    try:
        df = pd.read_excel(GIRIS_DOSYASI)
        print(f"✅ {len(df)} satır veri analize hazır.")
    except FileNotFoundError:
        print(f"❌ HATA: '{GIRIS_DOSYASI}' dosyası bulunamadı. Önce simülasyonu çalıştır!")
        return

    # Analiz Başlıyor
    sonuclar = []
    print("🕵️‍♂️ BERT yorumları okuyor...")
    
    # Yorumları liste haline getirip toplu verelim (Daha hızlı olur)
    yorumlar = df['Yorum'].astype(str).tolist()
    
    # TQDM ile ilerleme çubuğu
    for yorum in tqdm(yorumlar):
        # Yorum çok uzunsa BERT hata verebilir, ilk 512 karakteri alalım
        yorum_kisa = yorum[:512]
        try:
            sonuc = analizci(yorum_kisa)[0]
            # Sonuc şuna benzer: {'label': 'positive', 'score': 0.98}
            
            # Etiketi Türkçeleştir
            etiket = "Olumlu" if "positive" in sonuc['label'] else "Olumsuz"
            sonuclar.append({
                'BERT_Etiket': etiket,
                'BERT_Guven_Skoru': sonuc['score']
            })
        except Exception as e:
            sonuclar.append({'BERT_Etiket': 'Hata', 'BERT_Guven_Skoru': 0.0})

    # Sonuçları ana tabloya ekle
    df_sonuc = pd.concat([df, pd.DataFrame(sonuclar)], axis=1)
    
    # Kaydet
    df_sonuc.to_excel(CIKIS_DOSYASI, index=False)
    
    print(f"\n🎉 ANALİZ BİTTİ!")
    print(f"💾 Sonuçlar kaydedildi: {CIKIS_DOSYASI}")
    print("💡 İPUCU: Şimdi 'BERT_Etiket' sütununa bakarak yapay zekanın kararlarını inceleyebilirsin.")

if __name__ == "__main__":
    bert_ile_analiz_et()