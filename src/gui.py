import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

DATA_DIR = "../data"

def yukle_veri():
    # Önce video bilgilerini oku
    video_path = os.path.join(DATA_DIR, "video_bilgileri.csv")
    yorum_path = os.path.join(DATA_DIR, "yorumlar.csv")

    # Video bilgileri
    try:
        video_df = pd.read_csv(video_path)
        if video_df.empty:
            raise ValueError("video_bilgileri.csv boş görünüyor.")

        v = video_df.iloc[0]

        lbl_baslik_val.config(text=v.get("video_baslik", "-"))
        lbl_kanal_val.config(text=v.get("kanal_adi", "-"))
        lbl_tarih_val.config(text=v.get("yayim_tarihi", "-"))
        lbl_view_val.config(text=str(v.get("goruntulenme_sayisi", "-")))
        lbl_like_val.config(text=str(v.get("begeni_sayisi", "-")))
        lbl_comment_val.config(text=str(v.get("yorum_sayisi", "-")))

    except Exception as e:
        messagebox.showerror(
            "Hata",
            f"Video bilgileri yüklenirken hata oluştu:\n{e}\n\n"
            f"Lütfen önce yorum_cek.py dosyasını çalıştırdığından emin ol."
        )

    # Yorumlar
    try:
        df = pd.read_csv(yorum_path)
    except Exception as e:
        messagebox.showerror(
            "Hata",
            f"Yorumlar yüklenirken hata oluştu:\n{e}\n\n"
            f"Lütfen önce yorum_cek.py dosyasını çalıştırdığından emin ol."
        )
        return

    listbox.delete(0, tk.END)
    for _, row in df.iterrows():
        yorum_yapan = str(row.get("yorum_yapan", "Bilinmiyor"))
        yorum = str(row.get("yorum", ""))
        listbox.insert(tk.END, f"{yorum_yapan}: {yorum}")


# ----- PENCERE -----
pencere = tk.Tk()
pencere.title("Video Yorum Görüntüleyici")
pencere.geometry("900x600")

# Üst kısım: Video bilgileri
frame_video = tk.Frame(pencere, padx=10, pady=10)
frame_video.pack(fill=tk.X)

tk.Label(frame_video, text="Video Başlığı:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
lbl_baslik_val = tk.Label(frame_video, text="-")
lbl_baslik_val.grid(row=0, column=1, sticky="w")

tk.Label(frame_video, text="Kanal:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w")
lbl_kanal_val = tk.Label(frame_video, text="-")
lbl_kanal_val.grid(row=1, column=1, sticky="w")

tk.Label(frame_video, text="Yayın Tarihi:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w")
lbl_tarih_val = tk.Label(frame_video, text="-")
lbl_tarih_val.grid(row=2, column=1, sticky="w")

tk.Label(frame_video, text="Görüntülenme:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w", padx=(30,0))
lbl_view_val = tk.Label(frame_video, text="-")
lbl_view_val.grid(row=0, column=3, sticky="w")

tk.Label(frame_video, text="Beğeni:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky="w", padx=(30,0))
lbl_like_val = tk.Label(frame_video, text="-")
lbl_like_val.grid(row=1, column=3, sticky="w")

tk.Label(frame_video, text="Yorum Sayısı:", font=("Arial", 10, "bold")).grid(row=2, column=2, sticky="w", padx=(30,0))
lbl_comment_val = tk.Label(frame_video, text="-")
lbl_comment_val.grid(row=2, column=3, sticky="w")

# Buton
buton = tk.Button(pencere, text="Video Bilgileri ve Yorumları Yükle", command=yukle_veri)
buton.pack(pady=5)

# Alt kısım: Yorum listesi + scrollbar
frame_list = tk.Frame(pencere)
frame_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_list, width=120, height=25, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=listbox.yview)

pencere.mainloop()
