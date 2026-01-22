import tkinter as tk
from tkinter import messagebox
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import random

# --- AYARLAR ---
MODEL_YOLU = "./final_model"
TEST_VERISI = "ham_veriler/test_seti_30.xlsx"

class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Can'ın Tez Projesi - Duygu Analizi v1.0")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        # Başlık
        title_label = tk.Label(root, text="TÜRKÇE ÜRÜN YORUMLARI ANALİZİ\n(BERT Model)", 
                               font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=20)

        # Durum
        self.status_label = tk.Label(root, text="Model Yükleniyor...", font=("Arial", 10), fg="orange", bg="#f0f0f0")
        self.status_label.pack()

        # Giriş Alanı
        self.text_input = tk.Text(root, height=5, width=60, font=("Arial", 11))
        self.text_input.pack(pady=10)

        # Butonlar
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        self.analyze_btn = tk.Button(btn_frame, text="ANALİZ ET 🔍", command=self.analiz_et, 
                                     font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15, state="disabled")
        self.analyze_btn.pack(side=tk.LEFT, padx=10)

        self.random_btn = tk.Button(btn_frame, text="Rastgele Yorum 🎲", command=self.rastgele_getir, 
                                    font=("Arial", 11), bg="#2196F3", fg="white")
        self.random_btn.pack(side=tk.LEFT, padx=10)

        # Sonuç Alanı
        self.result_frame = tk.Frame(root, bg="white", relief="sunken", bd=2)
        self.result_frame.pack(pady=20, fill="x", padx=40)

        self.lbl_duygu = tk.Label(self.result_frame, text="Sonuç Bekleniyor...", font=("Helvetica", 18, "bold"), bg="white", fg="#999")
        self.lbl_duygu.pack(pady=10)

        self.lbl_skor = tk.Label(self.result_frame, text="", font=("Arial", 10), bg="white")
        self.lbl_skor.pack(pady=5)

        # Modeli Yükle (Gecikmeli)
        self.root.after(100, self.modeli_yukle)

    def modeli_yukle(self):
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_YOLU)
            self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_YOLU)
            self.model.to(self.device)
            
            # Test verisi (Rastgele tuşu için)
            try:
                self.df_test = pd.read_excel(TEST_VERISI)
                self.df_test = self.df_test.dropna(subset=['yorum'])
            except:
                self.df_test = pd.DataFrame({'yorum': ["Veri dosyası bulunamadı."]})

            self.status_label.config(text=f"✅ Model Hazır! ({self.device})", fg="green")
            self.analyze_btn.config(state="normal")
        except Exception as e:
            self.status_label.config(text=f"❌ Model Yüklenemedi! (Eğitim bitmemiş olabilir)", fg="red")

    def analiz_et(self):
        yorum = self.text_input.get("1.0", tk.END).strip()
        if not yorum: return

        inputs = self.tokenizer(yorum, return_tensors="pt", truncation=True, padding=True, max_length=128).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            tahmin_idx = torch.argmax(probs).item()
            guven = probs[0][tahmin_idx].item()

        etiketler = {0: "NEGATİF 😡", 1: "NÖTR 😐", 2: "POZİTİF 😊"}
        renkler = {0: "#ffcccc", 1: "#ffffcc", 2: "#ccffcc"}
        yazi_renk = {0: "#cc0000", 1: "#999900", 2: "#006600"}

        sonuc_metni = etiketler.get(tahmin_idx, "Bilinmiyor")
        
        self.lbl_duygu.config(text=sonuc_metni, fg=yazi_renk.get(tahmin_idx, "black"))
        self.result_frame.config(bg=renkler.get(tahmin_idx, "white"))
        self.lbl_duygu.config(bg=renkler.get(tahmin_idx, "white"))
        self.lbl_skor.config(text=f"Güven Skoru: %{guven*100:.1f}", bg=renkler.get(tahmin_idx, "white"))

    def rastgele_getir(self):
        if not self.df_test.empty:
            rastgele = random.choice(self.df_test['yorum'].tolist())
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", rastgele)

if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentApp(root)
    root.mainloop()