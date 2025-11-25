import nltk
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")

stopwords_tr = stopwords.words("turkish")

def temizle(text):
    # Boş / NaN / string olmayan değerleri yakala
    if not isinstance(text, str):
        return []  # boş token listesi döndür

    text = text.lower()
    # Harfler ve boşluk dışındaki her şeyi sil
    text = re.sub(r"[^a-zçğıöşüı ]", " ", text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords_tr and len(t) > 1]
    return tokens

def cumle_vektoru(tokens, model):
    v = []
    for t in tokens:
        if t in model.wv:
            v.append(model.wv[t])
    if len(v) == 0:
        return np.zeros(model.vector_size)
    return np.mean(v, axis=0)
