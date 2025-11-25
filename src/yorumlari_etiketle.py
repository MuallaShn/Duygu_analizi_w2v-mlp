import pandas as pd

def yorumlari_etiketle():
    df = pd.read_csv("../data/yorumlar.csv")

    # Kaç yorum etiketlemek istiyorsun? (örneğin 50)
    N = 45
    df = df.head(N).copy()

    etiketler = []
    print("Yorumları sırayla göstereceğim.")
    print("Etiket gir: p = pozitif, n = negatif, o = notr, s = skip\n")

    for i, row in df.iterrows():
        yorum = str(row["yorum"])
        print("-" * 80)
        print(f"{i}: {yorum}")
        while True:
            e = input("Etiket (p/n/o/s): ").strip().lower()
            if e in ["p", "n", "o", "s"]:
                break
            else:
                print("Lütfen sadece p / n / o / s gir.")

        if e == "p":
            etiketler.append("pozitif")
        elif e == "n":
            etiketler.append("negatif")
        elif e == "o":
            etiketler.append("notr")
        else:  # s = skip
            etiketler.append(None)

    df["gercek_etiket"] = etiketler
    df = df.dropna(subset=["gercek_etiket"])  # skip edilenleri at

    df.to_csv("../data/yorumlar_etiketli.csv", index=False, encoding="utf-8")
    print("\nEtiketleme bitti. yorumlar_etiketli.csv kaydedildi.")

if __name__ == "__main__":
    yorumlari_etiketle()
