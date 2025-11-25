import os
import pandas as pd
import numpy as np
import joblib

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

from gensim.models import Word2Vec
from preprocessing import temizle, cumle_vektoru

def train_mlp():
    # 1) Eğitim setini oku
    df = pd.read_csv("../data/egitim_seti.csv")

    # Sütun adların: 'text' (metin), 'category' (etiket)
    metinler = df["text"]
    etiketler = df["category"]

    # 2) Word2Vec modelini yükle (önce word2vec_train.py çalışmış olmalı)
    w2v = Word2Vec.load("../models/w2v.model")

    # 3) Her metin için cümle vektörü oluştur
    X_list = []
    for s in metinler:
        tokens = temizle(s)
        v = cumle_vektoru(tokens, w2v)
        X_list.append(v)

    X = np.vstack(X_list)
    y = etiketler.values

    # 4) Eğitim / test ayır
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print(f"Eğitim örnek sayısı: {X_train.shape[0]}")
    print(f"Test örnek sayısı   : {X_test.shape[0]}")

    # ---------------------------------------------------
    # MODEL 1  (şu anki modelin)
    # ---------------------------------------------------
    clf1 = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        max_iter=300,
        random_state=42
    )

    clf1.fit(X_train, y_train)
    y_pred1 = clf1.predict(X_test)

    print("\n=== MODEL 1 SONUÇLARI ===")
    print("Parametreler: hidden_layer_sizes=(64,32), activation='relu', max_iter=300")
    print("\nHATA MATRİSİ (Model 1):")
    print(confusion_matrix(y_test, y_pred1))

    print("\nMETRİKLER (Model 1):")
    print(classification_report(y_test, y_pred1))

    # Model 1'i kaydet (tahmin.py şu modeli kullanmaya devam etsin)
    os.makedirs("../models", exist_ok=True)
    joblib.dump(clf1, "../models/mlp_model.pkl")
    print("Model 1 ../models/mlp_model.pkl olarak kaydedildi.")

    # ---------------------------------------------------
    # MODEL 2  (parametreleri değiştirilmiş model)
    # ---------------------------------------------------
    clf2 = MLPClassifier(
        hidden_layer_sizes=(128, 64),
        activation="tanh",   # farklı aktivasyon
        max_iter=400,        # daha fazla iterasyon
        random_state=42
    )

    clf2.fit(X_train, y_train)
    y_pred2 = clf2.predict(X_test)

    print("\n=== MODEL 2 SONUÇLARI ===")
    print("Parametreler: hidden_layer_sizes=(128,64), activation='tanh', max_iter=400")
    print("\nHATA MATRİSİ (Model 2):")
    print(confusion_matrix(y_test, y_pred2))

    print("\nMETRİKLER (Model 2):")
    print(classification_report(y_test, y_pred2))

    # Model 2'yi de ayrı dosyaya kaydedelim (istersen bunu da kullanabilirsin)
    joblib.dump(clf2, "../models/mlp_model_v2.pkl")
    print("Model 2 ../models/mlp_model_v2.pkl olarak kaydedildi.")

if __name__ == "__main__":
    train_mlp()
