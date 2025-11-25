from gensim.models import Word2Vec
import pandas as pd
from preprocessing import temizle

def train_w2v():
    df = pd.read_csv("../data/yorumlar.csv")
    tokenized = [temizle(y) for y in df["yorum"]]
    # boş listeleri filtrele
    tokenized = [t for t in tokenized if len(t) > 0]

    model = Word2Vec(
        sentences=tokenized,
        vector_size=100,
        window=5,
        min_count=2,
        sg=1
    )

    model.save("../models/w2v.model")
    print("w2v.model kaydedildi.")

if __name__ == "__main__":
    train_w2v()
