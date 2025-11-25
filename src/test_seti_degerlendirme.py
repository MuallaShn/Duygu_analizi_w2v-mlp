import pandas as pd
import numpy as np
import joblib
from gensim.models import Word2Vec
from sklearn.metrics import confusion_matrix, classification_report
from preprocessing import temizle, cumle_vektoru

def kendi_test_seti_degerlendir():
    # 1) Elle etiketlediğin dosya
    df = pd.read_csv("../data/yorumlar_etiketli.csv")

    # 2) Model ve Word2Vec
    clf = joblib.load("../models/mlp_model.pkl")
    w2v = Word2Vec.load("../models/w2v.model")

    # 3) Yorumları sayısallaştır
    X_list = []
    for y in df["yorum"]:
        v = cumle_vektoru(temizle(y), w2v)
        X_list.append(v)
    X = np.vstack(X_list)

    y_true = df["gercek_etiket"].values
    y_pred = clf.predict(X)

    print("=== KENDİ YOUTUBE TEST SETİN ===")
    print("\nHATA MATRİSİ:")
    print(confusion_matrix(y_true, y_pred))

    print("\nMETRİKLER:")
    print(classification_report(y_true, y_pred))

    df["tahmin"] = y_pred
    df.to_csv("../data/yorumlar_etiketli_sonuclu.csv", index=False, encoding="utf-8")
    print("yorumlar_etiketli_sonuclu.csv kaydedildi.")

if __name__ == "__main__":
    kendi_test_seti_degerlendir()
