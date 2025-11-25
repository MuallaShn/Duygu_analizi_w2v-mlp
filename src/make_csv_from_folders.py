import os
import pandas as pd


BASE_DIR = r"C:\Users\Mualla\Downloads\film_yorumlari\film_yorumlari\raw_texts"

# 2) Klasör adı -> etiket ismi eşlemesi
label_map = {
    "pozitif": "pozitif",
    "negatif": "negatif",
    "tarafsiz": "notr",   # klasörün adı "tarafsız" ise, Windows bunu genelde "tarafsiz" gibi tutar
}

rows = []

for folder_name, label in label_map.items():
    folder_path = os.path.join(BASE_DIR, folder_name)

    # Klasör yoksa uyarı ver
    if not os.path.isdir(folder_path):
        print(f"Uyarı: {folder_path} klasörü bulunamadı, ismi farklı olabilir.")
        continue

    for fname in os.listdir(folder_path):
        # sadece .txt dosyalarını al
        if not fname.lower().endswith(".txt"):
            continue

        fpath = os.path.join(folder_path, fname)

        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()

        rows.append({
            "text": text,
            "category": label,   # pozitif / negatif / notr
        })

# pandas ile DataFrame oluştur
df = pd.DataFrame(rows, columns=["text", "category"])
print(df.head())
print("Toplam örnek sayısı:", len(df))

# 3) Bunu projenin data klasörüne kaydet
os.makedirs("../data", exist_ok=True)
df.to_csv("../data/egitim_seti.csv", index=False, encoding="utf-8")
print("egitim_seti.csv ../data klasörüne kaydedildi.")
