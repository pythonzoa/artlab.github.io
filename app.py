import streamlit as st
import speech_recognition as sr
import cv2
from pathlib import Path
import time

# 페이지 기본 설정
st.set_page_config(page_title="아트랩 음성 인식 갤러리", layout="wide")

# 파일 경로 설정
BACKGROUND_IMAGE_PATH = "images/HyundaiArtlab.png"
VIDEO_PATH_JUNG = "videos/MMCA.mp4"
IMAGE_PATH_KIM = "images/지원.jpg"

# 헤더 영역
col1, col2 = st.columns([3, 1])
with col2:
    st.image(BACKGROUND_IMAGE_PATH, width=200)

# 중앙 메시지
st.markdown("<h1 style='text-align: center;'>안녕하세요^^ 아트랩입니다</h1>", unsafe_allow_html=True)

# 음성 인식 기능
def listen_for_artist():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("음성을 듣는 중...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='ko-KR')
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            st.error("음성 인식 서비스에 문제가 있습니다.")
            return None

# 메인 컨텐츠 영역
if st.button("작가 이름 말하기"):
    result = listen_for_artist()
    if result:
        st.write(f"인식된 텍스트: {result}")
        if "정연두" in result:
            st.video(VIDEO_PATH_JUNG)
            st.write("정연두 작가의 작품입니다")
        elif "김지원" in result:
            st.image(IMAGE_PATH_KIM)
            st.write("김지원 작가 / 3층 / 맛있는 식사에 대하여")

# 하단 안내 메시지
st.markdown("""
<div style='position: fixed; bottom: 20px; right: 20px; color: gray;'>
작가의 이름을 말씀해주세요 :)
</div>
""", unsafe_allow_html=True)
