import pandas as pd
import joblib
from gensim.models import Word2Vec
from preprocessing import temizle, cumle_vektoru

def tahmin_yap():
    df = pd.read_csv("../data/yorumlar.csv")
    clf = joblib.load("../models/mlp_model.pkl")
    w2v = Word2Vec.load("../models/w2v.model")

    df["tahmin"] = df["yorum"].apply(lambda y: clf.predict([cumle_vektoru(temizle(y), w2v)])[0])

    df.to_csv("../data/tahminli_yorumlar.csv", index=False)
    print("tahminli_yorumlar.csv oluşturuldu.")

if __name__ == "__main__":
    tahmin_yap()
