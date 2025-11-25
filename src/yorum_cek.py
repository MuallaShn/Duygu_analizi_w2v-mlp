from googleapiclient.discovery import build
import pandas as pd

API_KEY = "AIzaSyBq_EfVDxCezs5UOqmfm37hhyHrobI2Els"
VIDEO_ID = "_wZUNiGtkcw"  # senin video ID'n

def video_bilgisi_cek(youtube):
    response = youtube.videos().list(
        part="snippet,statistics",
        id=VIDEO_ID
    ).execute()

    item = response["items"][0]
    snippet = item["snippet"]
    stats = item["statistics"]

    video_info = {
        "video_id": VIDEO_ID,
        "video_baslik": snippet["title"],
        "kanal_adi": snippet["channelTitle"],
        "yayim_tarihi": snippet["publishedAt"],
        "goruntulenme_sayisi": stats.get("viewCount"),
        "begeni_sayisi": stats.get("likeCount"),
        "yorum_sayisi": stats.get("commentCount"),
    }

    df = pd.DataFrame([video_info])
    df.to_csv("../data/video_bilgileri.csv", index=False, encoding="utf-8")
    print("video_bilgileri.csv oluşturuldu.")


def yorum_cek():
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Önce video bilgilerini çek
    video_bilgisi_cek(youtube)

    comments = []
    next_page = None

    while True:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=VIDEO_ID,
            maxResults=100,
            pageToken=next_page,
            textFormat="plainText"
        ).execute()

        for item in response["items"]:
            thread_snippet = item["snippet"]
            snippet = thread_snippet["topLevelComment"]["snippet"]

            comments.append({
                "video_id": VIDEO_ID,
                "yorum_id": item["id"],
                "yorum": snippet["textOriginal"],
                "yorum_tarih": snippet["publishedAt"],
                "yorum_yapan": snippet["authorDisplayName"],
                "yorum_begeni_sayisi": snippet["likeCount"],
                "yanit_sayisi": thread_snippet.get("totalReplyCount", 0),

                # Yorum yapan kullanıcının görünür bilgileri:
                "yorum_yapan_kanal_id": snippet.get("authorChannelId", {}).get("value"),
                "yorum_yapan_kanal_url": snippet.get("authorChannelUrl"),
                "yorum_yapan_profil_resmi": snippet.get("authorProfileImageUrl"),

                # Dislike API'de yok, raporda özellikle belirt
                "yorum_dislike_sayisi": None
            })

        next_page = response.get("nextPageToken")
        if not next_page:
            break

    df = pd.DataFrame(comments)
    df.to_csv("../data/yorumlar.csv", index=False, encoding="utf-8")
    print("yorumlar.csv oluşturuldu.")


if __name__ == "__main__":
    yorum_cek()
