import streamlit as st
import speech_recognition as sr
import cv2
import numpy as np
from PIL import Image
import time

# 파일 경로 설정
BACKGROUND_IMAGE_PATH = "images/HyundaiArtlab.png"
VIDEO_PATH_JUNG = "videos/MMCA.mp4"
IMAGE_PATH_KIM = "images/지원.jpg"

# 페이지 설정
st.set_page_config(page_title="아트랩", layout="wide")

# 배경 이미지 (우측 상단)
col1, col2 = st.columns([3, 1])
with col2:
    st.image(BACKGROUND_IMAGE_PATH, width=200)

# 중앙 메시지
st.markdown(
    f"<div style='text-align: center; font-size: 24px;'>안녕하세요^^ 아트랩입니다</div>", 
    unsafe_allow_html=True
)

def listen_for_artists():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("음성을 듣는 중...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='ko-KR')
            return text
        except Exception as e:
            st.error(f"음성 인식 중 오류 발생: {str(e)}")
            return None

# 메인 섹션
if st.button("작가 이름 말하기"):
    text = listen_for_artists()
    if text:
        st.write(f"인식된 텍스트: {text}")
        if "정연두" in text:
            st.video(VIDEO_PATH_JUNG)
            st.write("정연두 작가의 작품입니다")
        elif "김지원" in text:
            st.image(IMAGE_PATH_KIM)
            st.write("김지원 작가 / 3층 / 맛있는 식사에 대하여")

# 하단 안내 메시지
st.markdown(
    "<div style='position: fixed; bottom: 20px; right: 20px; color: gray;'>작가의 이름을 불러주세요:)</div>",
    unsafe_allow_html=True
)
