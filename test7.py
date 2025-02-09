공유하기


나의 말:
import pygame
import cv2
import numpy as np
import speech_recognition as sr
import threading
import os
import time

# 파일 경로 설정
BACKGROUND_IMAGE_PATH = r"C:\Users\TMS\Downloads\HyundaiArtlab.png"
VIDEO_PATH_JUNG = r"C:\Users\TMS\Downloads\MMCA.mp4"
IMAGE_PATH_KIM = r"C:\Users\TMS\Downloads\지원.jpg"

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
image_surface = None  # 현재 표시 중인 이미지
is_fading_out = False  # 페이드 아웃 완료 여부
hide_ui = False  # 로고 및 힌트 숨김 여부

# 흐르는 문구 상태
scroll_text = "안녕하세요^^ 아트랩입니다"
scroll_x = WINDOW_WIDTH
scroll_speed = 5

# 우측 하단 작은 안내 문구
hint_text = "작가의 이름을 불러주세요:)"
hint_x = WINDOW_WIDTH - 250
hint_y = WINDOW_HEIGHT - 50


def listen_for_trigger():
    """음성을 감지하고 특정 단어가 감지되면 미디어를 표시."""
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
                    fade_direction = 1  # 페이드 인 시작
                    media_to_display = WORDS_TO_TRIGGER[text]["media"]
                    media_start_time = time.time()
                    is_fading_out = False  # 미디어가 끝났음을 나타내는 변수
                    hide_ui = True

                    # 이미지 미리 로드
                    if media_to_display.endswith(".mp4"):
                        image_surface = None
                    else:
                        image_surface = pygame.image.load(media_to_display)
                        image_surface = pygame.transform.scale(image_surface, (400, 300))

            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except sr.RequestError as e:
                print(f"오류 발생: {e}")


def play_video(video_path, display_text):
    """Pygame에서 OpenCV 비디오를 재생하며 텍스트를 함께 표시"""
    cap = cv2.VideoCapture(video_path)
    clock = pygame.time.Clock()

    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale_factor = min(WINDOW_WIDTH / original_width, WINDOW_HEIGHT / original_height)
    new_width, new_height = int(original_width * scale_factor), int(original_height * scale_factor)

    font = pygame.font.Font(font_path, 40) if font_path else pygame.font.SysFont('Arial', 40)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # 좌우 반전
        frame = cv2.resize(frame, (new_width, new_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)

        screen.fill((255, 255, 255))
        screen.blit(frame, ((WINDOW_WIDTH - new_width) // 2, (WINDOW_HEIGHT - new_height) // 2))

        # 🔹 텍스트 추가 (영상 위에 표시)
        text_surface = font.render(display_text, True, (0, 0, 0))  # 흰색 글씨
        screen.blit(text_surface, (40, 30))

        pygame.display.flip()
        pygame.event.pump()
        clock.tick(30)

    cap.release()



def main_loop():
    """Pygame 메인 루프"""
    global fade_alpha, fade_direction, media_to_display, media_start_time, current_text, scroll_x, image_surface, is_fading_out, hide_ui
    clock = pygame.time.Clock()
    threading.Thread(target=listen_for_trigger, daemon=True).start()

    while True:
        screen.fill((255, 255, 255))

        # 흐르는 문구 & 현대차 로고 & 힌트 텍스트 (미디어가 없을 때만 표시)
        if media_to_display is None and not is_fading_out:
            # HyundaiArtlab 로고 배치
            screen.blit(background, (WINDOW_WIDTH - 220, 20))

            # 흐르는 문구
            scroll_surface = font.render(scroll_text, True, (0, 0, 0))
            screen.blit(scroll_surface, (scroll_x, 250))
            scroll_x -= scroll_speed
            if scroll_x + scroll_surface.get_width() < 0:
                scroll_x = WINDOW_WIDTH  # 오른쪽에서 다시 시작

            # 힌트 텍스트 표시
            hint_surface = small_font.render(hint_text, True, (0, 0, 0))  # ✅ 검정색 힌트 텍스트
            screen.blit(hint_surface, (hint_x, hint_y))  # ✅ 미디어 종료 후 확실히 힌트 표시

        # 페이드 인/아웃 효과 적용
        if fade_direction == 1:  # 페이드 인
            fade_alpha = min(255, fade_alpha + 5)
            if fade_alpha == 255:
                fade_direction = 0
        elif fade_direction == -1:  # 페이드 아웃
            fade_alpha = max(0, fade_alpha - 5)
            if fade_alpha == 0:
                fade_direction = 0
                current_text = ""
                media_to_display = None  # 🔥 페이드 아웃이 완료되면 미디어 제거
                is_fading_out = False  # 흐르는 문구 다시 표시

        # 미디어 표시
        if media_to_display:
            if media_to_display.endswith(".mp4"):
                play_video(media_to_display, WORDS_TO_TRIGGER[current_text]["text"])
                fade_direction = -1
            else:
                if image_surface:
                    image_surface.set_alpha(fade_alpha)
                    screen.blit(image_surface, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 150))

                # 10초 후 페이드 아웃 시작
                if time.time() - media_start_time > 10:
                    fade_direction = -1  # 페이드 아웃 시작
                    is_fading_out = True  # 이미지가 사라졌음을 나타내는 플래그

        # 감지된 단어에 해당하는 문구 표시
        if current_text in WORDS_TO_TRIGGER:
            text_surface = font.render(WORDS_TO_TRIGGER[current_text]["text"], True, (0, 0, 0))
            text_surface.set_alpha(fade_alpha)
            screen.blit(text_surface, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main_loop()
