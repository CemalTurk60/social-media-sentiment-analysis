import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# --- DOSYALAR ---
VERI_DOSYASI = "ml_hazir_veri.csv"
MODEL_DOSYASI = "sentiment_model.pkl"
VEKTOR_DOSYASI = "tfidf_vectorizer.pkl"

def model_egit():
    print("🚀 Model Eğitimi Başlıyor...")
    
    # 1. Veriyi Yükle
    try:
        df = pd.read_csv(VERI_DOSYASI)
    except FileNotFoundError:
        print("❌ HATA: Önce 'ml_preprocessing.py' dosyasını çalıştırıp veriyi hazırla!")
        return

    # 2. X ve y Ayrımı
    X = df['Temiz_Yorum'] # Girdi (Metin)
    y = df['Hedef']       # Çıktı (1: Olumlu, 0: Olumsuz)
    
    # 3. Eğitim ve Test Seti Ayrımı (%80 Eğitim, %20 Test)
    print("✂️ Veri seti ayrılıyor (%80 Eğitim - %20 Test)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Vektörleştirme (TF-IDF)
    # Bilgisayar kelimeden anlamaz, sayıya çeviriyoruz.
    print("🔢 Metinler sayılara dönüştürülüyor (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=2000) # En çok kullanılan 2000 kelimeyi al
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Vektörleyiciyi kaydet (İleride yeni yorum gelince kullanacağız)
    pickle.dump(vectorizer, open(VEKTOR_DOSYASI, "wb"))
    
    # 5. Model Eğitimi (Logistic Regression)
    print("🧠 Yapay Zeka (Logistic Regression) eğitiliyor...")
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)
    
    # Modeli kaydet
    pickle.dump(model, open(MODEL_DOSYASI, "wb"))
    print(f"💾 Model kaydedildi: {MODEL_DOSYASI}")
    
    # 6. Performans Testi
    print("\n--- 📊 MODEL PERFORMANS RAPORU ---")
    y_pred = model.predict(X_test_vec)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Doğruluk Oranı (Accuracy): %{acc*100:.2f}")
    
    print("\n🔍 Detaylı Rapor:")
    print(classification_report(y_test, y_pred, target_names=['Olumsuz', 'Olumlu']))
    
    # 7. Karmaşıklık Matrisi (Confusion Matrix) Grafiği
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Olumsuz', 'Olumlu'], yticklabels=['Olumsuz', 'Olumlu'])
    plt.title('Model Başarısı (Confusion Matrix)')
    plt.ylabel('Gerçek Durum')
    plt.xlabel('Model Tahmini')
    plt.savefig('ml_basari_grafigi.png')
    print("📈 Başarı grafiği kaydedildi: ml_basari_grafigi.png")

if __name__ == "__main__":
    model_egit()