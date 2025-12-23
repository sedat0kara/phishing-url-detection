# 🎣 Phishing URL Detection with Machine Learning

Bu proje, siber güvenlik farkındalığı kapsamında geliştirilmiş, URL adreslerinin güvenli mi yoksa oltalama (phishing) amaçlı mı olduğunu tespit eden hibrit bir yapay zeka uygulamasıdır.

Proje, **Python** ve **Scikit-learn** kütüphanelerini kullanarak **Multinomial Naive Bayes** algoritması ile eğitilmiştir. Ayrıca bilinen güvenli siteler için bir Whitelist (Beyaz Liste) mekanizması içerir.

## 🚀 Özellikler

* **Makine Öğrenmesi:** Geniş bir veri seti üzerinde TF-IDF ve Naive Bayes kullanılarak eğitilmiştir.
* **Gelişmiş Tokenization:** URL'leri anlamlı parçalara (token) ayırarak modelin hassasiyetini artırır.
* **Hibrit Tespit Sistemi:**
    * **Whitelist Kontrolü:** Popüler ve güvenli siteleri (Google, METU, E-Devlet vb.) anında tanır.
    * **AI Tahmini:** Bilinmeyen URL'ler için model olasılık hesabı yapar.
* **Görselleştirme:** Modelin başarısını ölçmek için Confusion Matrix (Hata Matrisi) grafiği oluşturur.

## 🛠 Gereksinimler

Projenin çalışması için aşağıdaki Python kütüphanelerine ihtiyaç vardır:
* pandas
* matplotlib
* seaborn
* scikit-learn
* tldextract

## 📦 Kurulum (Installation)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

**1. Projeyi İndirin:**
Terminali açın ve projeyi klonlayın:
```bash
git clone https://github.com/sedat0kara/phishing-url-detection.git
cd url-detection
```

**2. Gerekli Kütüphaneleri Yükleyin**
```bash
pip install -r requirements.txt
```

**3. Projeyi Çalıştırın**
```bash
python main.py
```

# 📝 Notlar

## Dosya yollarını kendi sisteminize göre düzenleyiniz

## Dataset kaynağı:

**Kaggle – https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls/code**

## Proje eğitim ve akademik amaçlıdır.
