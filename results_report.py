import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --- AYARLAR ---
TEST_DOSYASI = "ham_veriler/test_seti_30.xlsx"
MODEL_YOLU = "./final_model"  # Eğitilen modelin olduğu klasör

print("🚀 SONUÇ RAPORLAMA ARACI ÇALIŞIYOR...")

# 1. CİHAZ AYARI
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"   ⚙️ Çalışma Ortamı: {device}")

# 2. TEST VERİSİNİ YÜKLE
print("1. Test verisi yükleniyor...")
try:
    test_df = pd.read_excel(TEST_DOSYASI)
    # Etiketleri sayıya çevir
    label_map = {"Negatif": 0, "Nötr": 1, "Pozitif": 2}
    test_df['label'] = test_df['duygu'].map(label_map)
    # Temizlik
    test_df = test_df.dropna(subset=['label', 'yorum'])
    test_df['label'] = test_df['label'].astype(int)
    print(f"   ✅ {len(test_df)} adet test verisi hazır.")
except Exception as e:
    print(f"❌ Hata: Test dosyası okunamadı! {e}")
    exit()

# 3. EĞİTİLMİŞ MODELİ YÜKLE
print("2. Eğitilmiş BERT modeli yükleniyor...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_YOLU)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_YOLU)
    model.to(device)
    print("   ✅ Model başarıyla yüklendi.")
except Exception as e:
    print(f"❌ Hata: Model bulunamadı! Lütfen önce eğitimi tamamla. {e}")
    exit()

# 4. TAHMİN YAP (Prediction)
print("3. Model sınav oluyor (Tahminler yapılıyor)...")
preds = []
gercekler = test_df['label'].tolist()
yorumlar = test_df['yorum'].tolist()

model.eval()
batch_size = 16 

with torch.no_grad():
    for i in range(0, len(yorumlar), batch_size):
        batch_yorumlar = yorumlar[i:i+batch_size]
        inputs = tokenizer(batch_yorumlar, padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)
        preds.extend(predictions.cpu().numpy())
        
        if i % 500 == 0 and i > 0:
            print(f"   -> {i} yorum tamamlandı...")

print("   ✅ Tüm tahminler bitti!")

# --- RAPORLAMA VE GRAFİKLER ---

# Accuracy
accuracy = accuracy_score(gercekler, preds)
print(f"\n🏆 BERT MODELİ BAŞARISI (Accuracy): %{accuracy*100:.2f}")

# 1. Confusion Matrix
print("\n📊 Grafikler hazırlanıyor...")
plt.figure(figsize=(10, 8))
cm = confusion_matrix(gercekler, preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Negatif', 'Nötr', 'Pozitif'],
            yticklabels=['Negatif', 'Nötr', 'Pozitif'])
plt.title(f'BERT Türkçe Sentiment - Doğruluk: %{accuracy*100:.1f}', fontsize=16)
plt.ylabel('Gerçek Etiket')
plt.xlabel('Tahmin Edilen Etiket')
plt.tight_layout()
plt.savefig('bert_confusion_matrix.png', dpi=300)
print("   ✅ 'bert_confusion_matrix.png' kaydedildi!")

# 2. Sınıf Bazlı Performans Grafiği
report_dict = classification_report(gercekler, preds, target_names=['Negatif', 'Nötr', 'Pozitif'], output_dict=True)
class_performance = pd.DataFrame({
    'Sınıf': ['Negatif', 'Nötr', 'Pozitif'],
    'Precision': [report_dict['Negatif']['precision'], report_dict['Nötr']['precision'], report_dict['Pozitif']['precision']],
    'Recall': [report_dict['Negatif']['recall'], report_dict['Nötr']['recall'], report_dict['Pozitif']['recall']],
    'F1-Score': [report_dict['Negatif']['f1-score'], report_dict['Nötr']['f1-score'], report_dict['Pozitif']['f1-score']]
})

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(class_performance))
width = 0.25

ax.bar(x - width, class_performance['Precision'], width, label='Precision', color='#3498db')
ax.bar(x, class_performance['Recall'], width, label='Recall', color='#2ecc71')
ax.bar(x + width, class_performance['F1-Score'], width, label='F1-Score', color='#e74c3c')

ax.set_ylabel('Skor')
ax.set_title('Sınıf Bazlı Performans Değerleri')
ax.set_xticks(x)
ax.set_xticklabels(class_performance['Sınıf'])
ax.legend()
plt.tight_layout()
plt.savefig('bert_class_performance.png', dpi=300)
print("   ✅ 'bert_class_performance.png' kaydedildi!")

# 3. Örnek Tahminler Exceli
test_df['tahmin'] = preds
test_df['tahmin_duygu'] = test_df['tahmin'].map({0: 'Negatif', 1: 'Nötr', 2: 'Pozitif'})
test_df['dogru_mu'] = test_df['duygu'] == test_df['tahmin_duygu']

ornekler = pd.concat([
    test_df[test_df['dogru_mu'] == True].sample(min(10, len(test_df))),
    test_df[test_df['dogru_mu'] == False].sample(min(10, len(test_df)))
])
ornekler[['yorum', 'duygu', 'tahmin_duygu', 'dogru_mu']].to_excel('BERT_ANALIZ_ORNEKLERI.xlsx', index=False)
print("   ✅ 'BERT_ANALIZ_ORNEKLERI.xlsx' kaydedildi!")

print("\n✨ TÜM İŞLEMLER BİTTİ! Dosyalarına bakabilirsin. 🎓")