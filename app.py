import streamlit as st
import cv2
import numpy as np
from PIL import Image

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

# 음성 인식을 위한 JavaScript 코드
st.markdown("""
<script>
const recognition = new webkitSpeechRecognition();
recognition.lang = 'ko-KR';
recognition.continuous = false;

function startListening() {
    recognition.start();
}

recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    window.Streamlit.setComponentValue(text);
}
</script>
""", unsafe_allow_html=True)

# 작가 선택 버튼
if st.button("음성으로 작가 검색"):
    st.write("작가의 이름을 말씀해주세요:")
    # 여기서 JavaScript의 음성 인식 결과를 기다립니다
    if "정연두" in st.session_state.get('voice_input', ''):
        st.video(VIDEO_PATH_JUNG)
        st.write("정연두 작가의 작품입니다")
    elif "김지원" in st.session_state.get('voice_input', ''):
        st.image(IMAGE_PATH_KIM)
        st.write("김지원 작가 / 3층 / 맛있는 식사에 대하여")

# 또는 드롭다운으로 선택
artist = st.selectbox(
    "작가 선택",
    ["선택하세요", "정연두", "김지원"]
)

if artist == "정연두":
    st.video(VIDEO_PATH_JUNG)
    st.write("정연두 작가의 작품입니다")
elif artist == "김지원":
    st.image(IMAGE_PATH_KIM)
    st.write("김지원 작가 / 3층 / 맛있는 식사에 대하여")

# 하단 안내 메시지
st.markdown(
    "<div style='position: fixed; bottom: 20px; right: 20px; color: gray;'>작가의 이름을 불러주세요:)</div>",
    unsafe_allow_html=True
)
