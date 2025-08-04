import streamlit as st
from pytube import YouTube
import os
import glob

st.title('YouTube 下載器 🎬🎵')

# 清除暫存檔案，避免空間浪費
def clear_cache_files():
    files = glob.glob('dl_*')
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            st.warning(f"刪除檔案 {f} 失敗：{e}")

url = st.text_input('請輸入 YouTube 影片網址')

if url:
    try:
        yt = YouTube(url)
        st.success(f'影片標題：{yt.title}')

        # 選擇下載類型
        mode = st.radio("下載型式", ["影片（MP4）", "音樂（MP3）"])

        if mode == "影片（MP4）":
            videos = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            choices = [f"{s.resolution} - {round(s.filesize / 1024 / 1024, 2)}MB" for s in videos]
            index = st.selectbox("選擇影片品質", choices, index=0)
            selected_stream = videos[choices.index(index)]
        else:
            audios = yt.streams.filter(only_audio=True).order_by('abr').desc()
            choices = [f"{s.abr} - {round(s.filesize / 1024 / 1024, 2)}MB" for s in audios]
            index = st.selectbox("選擇音質", choices, index=0)
            selected_stream = audios[choices.index(index)]

        if st.button('下載'):
            clear_cache_files()
            with st.spinner('下載中...'):
                filepath = selected_stream.download(filename_prefix="dl_")
                if mode == "音樂（MP3）":
                    st.warning("下載的是音訊檔案，可將檔案副檔名從 .mp4 改成 .mp3 播放")
                st.success(f'下載完成，檔案位於：{filepath}')

    except Exception as e:
        st.error(f"下載失敗：{e}")
