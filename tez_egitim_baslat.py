import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import os

# --- AYARLAR ---
MODEL_ADI = "dbmdz/bert-base-turkish-cased"  # Kullanacağımız Türkçe BERT
EGITIM_DOSYASI = "ham_veriler/egitim_seti_70.xlsx"
TEST_DOSYASI = "ham_veriler/test_seti_30.xlsx"
CIKIS_KLASORU = "./final_model"  # Eğitilen model buraya kaydedilecek
EPOCH_SAYISI = 2  # Modeli kaç tur eğiteceğiz?

print("🚀 MODEL EĞİTİM SÜRECİ BAŞLIYOR (V2 - GÜNCELLENMİŞ)...")

# 1. VERİLERİ YÜKLE
print(f"1. Veri setleri yükleniyor...")
try:
    df_train = pd.read_excel(EGITIM_DOSYASI)
    df_test = pd.read_excel(TEST_DOSYASI)
    print(f"   ✅ Eğitim Verisi: {len(df_train)} | Test Verisi: {len(df_test)}")
except Exception as e:
    print(f"❌ Hata: Dosyalar bulunamadı! {e}")
    exit()

# 2. ETİKETLERİ SAYIYA ÇEVİR
label_map = {"Negatif": 0, "Nötr": 1, "Pozitif": 2}
df_train['label'] = df_train['duygu'].map(label_map)
df_test['label'] = df_test['duygu'].map(label_map)

# Temizlik
df_train = df_train.dropna(subset=['label', 'yorum'])
df_test = df_test.dropna(subset=['label', 'yorum'])
df_train['label'] = df_train['label'].astype(int)
df_test['label'] = df_test['label'].astype(int)

# 3. DATASET SINIFI
class YorumDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# 4. TOKENIZER VE MODEL
print("2. BERT Modeli hazırlanıyor...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ADI)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ADI, num_labels=3)

# Tokenize
print("3. Veriler işleniyor (Tokenization)...")
train_encodings = tokenizer(list(df_train['yorum']), truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(list(df_test['yorum']), truncation=True, padding=True, max_length=128)

train_dataset = YorumDataset(train_encodings, list(df_train['label']))
test_dataset = YorumDataset(test_encodings, list(df_test['label']))

# 5. EĞİTİM AYARLARI (GÜNCELLENDİ)
training_args = TrainingArguments(
    output_dir='./sonuclar',
    num_train_epochs=EPOCH_SAYISI,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    warmup_steps=100,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=50,
    eval_strategy="epoch",  # DÜZELTİLDİ: evaluation_strategy -> eval_strategy
    save_strategy="epoch",
    load_best_model_at_end=True,
    save_total_limit=1
)

# 6. BAŞLAT
print(f"\n🔥 EĞİTİM BAŞLIYOR! ({EPOCH_SAYISI} Epoch)")
print("   Bu işlem biraz sürebilir, arkana yaslan... ☕")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()

# 7. KAYDET
print(f"\n💾 Model kaydediliyor: {CIKIS_KLASORU}")
model.save_pretrained(CIKIS_KLASORU)
tokenizer.save_pretrained(CIKIS_KLASORU)

print("\n✨ TEBRİKLER! BERT ARTIK HAZIR! 🤖")