import streamlit as st
import yt_dlp
import glob
import os

st.title("YouTube 下載器（yt-dlp版）")

def clear_cache_files():
    files = glob.glob("dl_*")
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            st.warning(f"刪除檔案 {f} 失敗：{e}")

url = st.text_input("請輸入 YouTube 影片網址")

mode = st.radio("下載類型", ["影片（mp4）", "音樂（mp3）"])

if url:
    if st.button("下載"):
        clear_cache_files()
        with st.spinner("下載中..."):
            outtmpl = "dl_%(title)s.%(ext)s"
            ydl_opts = {
                "outtmpl": outtmpl,
                "quiet": True,
            }
            if mode == "影片（mp4）":
                ydl_opts["format"] = "best[ext=mp4]/best"
            else:
                ydl_opts["format"] = "bestaudio/best"
                ydl_opts["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                st.success("下載完成！請在本地目錄尋找下載的檔案。")
            except Exception as e:
                st.error(f"下載失敗：{e}")
