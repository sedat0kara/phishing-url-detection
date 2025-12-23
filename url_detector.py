import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tldextract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# ==========================================
# 1. VERİ SETİ YÜKLEME VE HAZIRLIK
# ==========================================
# Dosya yolunu kendi bilgisayarına göre güncellemelisin
dosya_yolu = r"C:\Users\sedat\Downloads\phishing_site_urls.csv\phishing_site_urls.csv"

print("Veri seti yükleniyor...")
data = pd.read_csv(dosya_yolu)

# Etiketleme: bad -> 1 (Phishing), good -> 0 (Güvenli)
data['Label'] = data['Label'].map({'bad': 1, 'good': 0})

# Dublike (tekrar eden) verileri temizleyelim (Modelin ezberlemesini önler)
#data = data.drop_duplicates()
#print(f"Temizlenmiş Veri Sayısı: {len(data)}")


# ==========================================
# 2. GELİŞMİŞ TOKENIZATION
# ==========================================
def make_tokens(url):
    # Daha hassas ayrıştırma: Sadece nokta ve tire değil, özel karakterleri de ayırır.
    # Örn: "amazon-security/login" -> ['amazon', 'security', 'login']
    tokens = str(url).replace('/', '.').replace('-', '.').replace('_', '.').replace('=', '.').split('.')
    # 'com', 'http', 'www' gibi çok yaygın ve ayırt edici olmayan kelimeleri atabiliriz (Stopwords mantığı)
    ignore_words = ['com', 'org', 'net', 'http', 'https', 'www']
    return [t for t in tokens if t and t not in ignore_words]


# ==========================================
# 3. VEKTÖRLEŞTİRME VE MODEL EĞİTİMİ
# ==========================================
print("Vektörleştirme yapılıyor...")
# ngram_range=(1,2) ekledik: Kelime gruplarını da öğrenir (örn: "secure login")
vectorizer = TfidfVectorizer(tokenizer=make_tokens, max_features=50000, ngram_range=(1, 2))

X = vectorizer.fit_transform(data['URL'])
y = data['Label']

# DÜZELTME 1: stratify=y
# Veri setindeki %72-%28 oranını eğitim ve test setinde de koruruz.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Model eğitiliyor...")
model = MultinomialNB()
model.fit(X_train, y_train)


# ==========================================
# 4. DETAYLI DEĞERLENDİRME VE GÖRSELLEŞTİRME
# ==========================================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Doğruluğu (Accuracy): %{accuracy * 100:.2f}")
print("\nSınıflandırma Raporu:")
print(classification_report(y_test, y_pred, target_names=["Güvenli", "Phishing"]))

# Confusion Matrix (Karmaşıklık Matrisi) Görselleştirmesi
# Tezin rapor kısmına bu grafiği koymalısın.
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Güvenli', 'Phishing'],
            yticklabels=['Güvenli', 'Phishing'])
plt.xlabel('Tahmin Edilen')
plt.ylabel('Gerçek Durum')
plt.title('Confusion Matrix (Hata Matrisi)')
plt.show()


# ==========================================
# 5. GÜVENLİ HİBRİT TAHMİN (Refactored)
# ==========================================
def nlp_tahmin_gelismis(url):
    # "google.com.calinti-site.com" gibi tuzakları yakalamak için domain kökünü buluyoruz.
    extracted = tldextract.extract(url)
    main_domain = f"{extracted.domain}.{extracted.suffix}"  # örn: google.com

    whitelist_domains = [
        'google.com', 'youtube.com', 'facebook.com', 'amazon.com',
        'wikipedia.org', 'metu.edu.tr', 'turkiye.gov.tr', 'whatsapp.com',
        'microsoft.com', 'twitter.com', 'instagram.com', 'apple.com', 'paypal.com'
    ]

    # Tam eşleşme kontrolü (Substring değil!)
    if main_domain in whitelist_domains:
        return "GÜVENLİ (Whitelist)", 0.0, "Yeşil"

    # Model Tahmini
    vector_input = vectorizer.transform([url])
    tahmin = model.predict(vector_input)[0]
    olasilik = model.predict_proba(vector_input)[0]
    guven = olasilik[tahmin] * 100

    if tahmin == 1:
        return "TEHLİKELİ (Phishing)", guven, "Kırmızı"
    else:
        return "GÜVENLİ (Temiz)", guven, "Mavi"


# ==========================================
# CANLI TEST
# ==========================================
print("\n" + "=" * 50)
print("CANLI TEST ")
print("=" * 50)

test_urls = [
    "http://apple-id-update-security-login.com",  # Phishing
    "https://www.google.com",  # Whitelist
    "https://www.google.com.security-check.xyz",  # Phishing (Whitelist'i atlatmaya çalışan)
    "http://secure-login.paypal-update.gq",  # Phishing
    "https://www.metu.edu.tr",  # Whitelist
    "http://google.com",  # Phishing potansiyeli
]

for link in test_urls:
    sonuc, guven, renk = nlp_tahmin_gelismis(link)

    if renk == "Yeşil":
        prefix = "[OK]  "
    elif renk == "Kırmızı":
        prefix = "[!!!] "
    else:
        prefix = "[...] "

    print(f"URL: {link}")
    print(f"{prefix}Sonuç: {sonuc}")
    if renk != "Yeşil":
        print(f"      Model Eminliği: %{guven:.1f}")
    print("-" * 40)