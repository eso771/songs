import re, os, requests
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, UnsupportedError, ExtractorError, ContentTooShortError, PostProcessingError
from eyed3 import load
from eyed3.id3.frames import ImageFrame
from youtube_search import YoutubeSearch
from Song import loop


def get_url(query):
    if query.startswith("https://you") or query.startswith("https://www.you"):
        if "watch" in query:
            return query
        else:
            if "?" in query:
                return re.sub(r'\?.*', '', query)
            else:
                return query
    else:
        return None


def is_tiktok_url(url: str) -> bool:
    return "tiktok.com" in url


def is_instagram_url(url: str) -> bool:
    return "instagram.com" in url


def get_yt_info_query(query: str):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        return None
    try:
        result = results[0]
    except:
        return None
    try:
        videoid = result["id"]
    except:
        return None
    title = result["title"]
    duration_min = result["duration"]
    thumbnail = result["thumbnails"][0].split("?")[0]
    link = f"https://youtu.be/{videoid}"
    return title, duration_min, thumbnail, videoid, link


def youtube_search(link):
    results = YoutubeSearch(link, max_results=1).to_dict()
    try:
        title = results[0]["title"]
        name = re.sub(r"\W+", " ", title)
    except:
        title = "Bilinməyən ad"
        name = "Bilinməyən ad"
    try:
        artist = results[0]["channel"]
    except:
        artist = "Bilinməyən kanal"
    duration_min = results[0]["duration"]
    thumbnail = results[0]["thumbnails"][0].split("?")[0]
    return title, name, artist, duration_min, thumbnail


ydl_opts = {
        "format": "bestaudio/best",
        "cookiefile": "music.txt",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }


def download_song(link, name):
    with YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        ydl.download([link])
        info = ydl.extract_info(link, download=False)
        os.rename(f"{info['id']}.mp3", f"{name}.mp3")
        audio_file = f"{name}.mp3"
        return audio_file


def download_social_video(url: str):
    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
        "format": "best",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            if not info_dict or "url" not in info_dict:
                return "❌Bu post video deyil və ya yükləmək mümkün deyil\n📌Yalnız TikTok və Instagram videolarını yükləyə bilirəm", False
            filepath = ydl.prepare_filename(info_dict)
        return True, filepath
    except DownloadError as e:
        err = str(e)
        if "There is no video in this post" in err or ("Unsupported URL" in err and "tiktok.com" in url):
            return "❌Bu post video deyil\n📌Yalnız TikTok və Instagram videolarını yükləyə bilirəm", False
        return f"❌Video yüklənə bilmədi: {err}", False
    except UnsupportedError:
        return "❌Bu link dəstəklənmir", False
    except ExtractorError:
        return "❌Platformada məlumat çıxarıla bilmir", False
    except ContentTooShortError:
        return "❌ Video tam yüklənmədi", False
    except PostProcessingError:
        return "❌Video işlənərkən problem yarandı", False
    except Exception as e:
        return f"❌Gözlənilməz xəta baş verdi: {e}", False


def download_thumbnail(name, thumbnail):
    try:
        thumb_name = f"{name}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        with open(thumb_name, "wb") as file:
            file.write(thumb.content)
    except:
        thumb_name = "bot.jpg"
    return thumb_name


def add_metadata(audio_file, title, artist, thumb_name):
    audio = load(audio_file)
    if audio.tag is None:
        audio.initTag()
    audio.tag.title = title
    audio.tag.artist = artist
    audio.tag.album = title
    with open(thumb_name, "rb") as img_file:
        img_data = img_file.read()
        audio.tag.images.set(ImageFrame.FRONT_COVER, img_data, "image/jpeg")
    audio.tag.save()


def remove_files(audio_file, thumb_name):
    if os.path.exists(audio_file):
        os.remove(audio_file)
    if thumb_name != "bot.jpg" and os.path.exists(thumb_name):
        os.remove(thumb_name)
