import pygame
import cv2
import numpy as np
import speech_recognition as sr
import threading
import os
import time

// 웹용 상대 경로로 변경
BACKGROUND_IMAGE_PATH = "images/HyundaiArtlab.png"
VIDEO_PATH_JUNG = "videos/MMCA.mp4"
IMAGE_PATH_KIM = "images/지원.jpg"

# 단어별 미디어 및 문구 설정
WORDS_TO_TRIGGER = {
    "정연두": {"media": VIDEO_PATH_JUNG, "text": "정연두 작가의 작품입니다"},
    "김지원": {"media": IMAGE_PATH_KIM, "text": "김지원 작가 / 3층 / 맛있는 식사에 대하여"}
}

# Pygame 초기화
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("꽃")


# 폰트 설정
def get_font_path():
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['WINDIR'], 'Fonts', 'HMKMMAG.TTF')
    return None


font_path = get_font_path()
font = pygame.font.Font(font_path, 40) if font_path else pygame.font.SysFont('Arial', 40)
small_font = pygame.font.Font(font_path, 20) if font_path else pygame.font.SysFont('Arial', 20)

# 배경 이미지 로드
background = pygame.image.load(BACKGROUND_IMAGE_PATH)
background = pygame.transform.scale(background, (200, 100))

# 상태 변수
current_text = ""
fade_alpha = 0
fade_direction = 0  # 1: 페이드 인, -1: 페이드 아웃, 0: 없음
media_to_display = None
media_start_time = None
image_surface = None
is_fading_out = False
hide_ui = False  # 현대차 로고 및 hint_text 숨김 여부

# 흐르는 문구 상태
scroll_text = "안녕하세요^^ 아트랩입니다"
scroll_x = WINDOW_WIDTH
scroll_speed = 5

# 우측 하단 작은 안내 문구
hint_text = "작가의 이름을 불러주세요:)"
hint_x = WINDOW_WIDTH - 250
hint_y = WINDOW_HEIGHT - 50


def listen_for_trigger():
    global current_text, fade_direction, media_to_display, media_start_time, image_surface, is_fading_out, hide_ui
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("음성을 듣는 중...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language='ko-KR')
                print("인식된 텍스트:", text)
                if text in WORDS_TO_TRIGGER:
                    current_text = text
                    fade_direction = 1
                    media_to_display = WORDS_TO_TRIGGER[text]["media"]
                    media_start_time = time.time()
                    is_fading_out = False
                    hide_ui = True  # 미디어 실행 시 UI 숨김
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except sr.RequestError as e:
                print(f"오류 발생: {e}")


def main_loop():
    global fade_alpha, fade_direction, media_to_display, media_start_time, current_text, image_surface, is_fading_out, hide_ui, scroll_x
    clock = pygame.time.Clock()
    threading.Thread(target=listen_for_trigger, daemon=True).start()
    while True:
        screen.fill((255, 255, 255))
        if not hide_ui:
            screen.blit(background, (WINDOW_WIDTH - 220, 20))
            hint_surface = small_font.render(hint_text, True, (100, 100, 100))
            screen.blit(hint_surface, (hint_x, hint_y))

        # 흐르는 문구 표시 (미디어가 없을 때만)
        if media_to_display is None and not is_fading_out:
            scroll_surface = font.render(scroll_text, True, (0, 0, 0))
            screen.blit(scroll_surface, (scroll_x, 250))
            scroll_x -= scroll_speed
            if scroll_x + scroll_surface.get_width() < 0:
                scroll_x = WINDOW_WIDTH  # 오른쪽에서 다시 시작

        if fade_direction == -1 and fade_alpha == 0:
            hide_ui = False
            media_to_display = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main_loop()
