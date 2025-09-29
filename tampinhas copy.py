import cv2
import numpy as np
import pygame
import time
from skimage import color

# Inicializa pygame mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

def beep(frequency=440, duration=150):
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate / 1000))
    t = np.linspace(0, duration / 1000, n_samples, False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio = np.array(wave * 32767, dtype=np.int16)
    stereo_sound = np.column_stack((audio, audio))
    sound = pygame.sndarray.make_sound(stereo_sound)
    sound.play()

# Paleta com 8 cores distintas (BGR)
color_groups_bgr = [
    (20, 20, 20),       # Preto
    (0, 0, 255),        # Vermelho
    (0, 165, 255),      # Laranja
    (0, 255, 255),      # Amarelo
    (0, 255, 0),        # Verde
    (255, 0, 0),        # Azul
    (128, 0, 128),      # Roxo
    (255, 255, 255)     # Branco
]

# Frequência base para cada grupo
base_frequencies = [300, 500, 700, 900, 1100, 1300, 1500, 1700]

# Converte BGR para LAB
color_groups_lab = np.array([
    color.rgb2lab(np.array([[list(reversed(c))]], dtype=np.uint8)/255.0)[0, 0]
    for c in color_groups_bgr
])

# Tolerância de cor LAB
tolerance = 2

# Inicialização da câmera
cap = cv2.VideoCapture(0)
last_beep_time = 0
beep_interval = 0.7  # segundos entre beeps

def color_distance_lab(c1, c2):
    return np.linalg.norm(c1 - c2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    num_groups = len(color_groups_bgr)
    rect_width = w // num_groups

    # Desenha faixas coloridas no topo da imagem (com transparência)
    for i, color_bgr in enumerate(color_groups_bgr):
        x1 = i * rect_width
        x2 = (i + 1) * rect_width
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, 0), (x2, h), color_bgr, -1)
        frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
        param1=100, param2=30, minRadius=20, maxRadius=80
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x, y, r) in circles[0, :1]:
            # Desenha o círculo detectado
            cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

            # Máscara circular para região da tampinha
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)

            # Calcula média de cor na região da tampinha
            mean_bgr = cv2.mean(frame, mask=mask)[:3]
            mean_lab = color.rgb2lab(np.array([[list(reversed(mean_bgr))]], dtype=np.uint8)/255.0)[0, 0]

            # Distância da cor detectada para cada grupo
            distances = [color_distance_lab(mean_lab, c) for c in color_groups_lab]
            closest_index = int(np.argmin(distances))
            closest_distance = distances[closest_index]

            # Ajusta frequência do beep
            if closest_distance <= tolerance:
                deviation = closest_distance / tolerance
                freq = base_frequencies[closest_index] + (1 - deviation) * 100
            else:
                freq = base_frequencies[closest_index] - 100

            # Emite beep com intervalo
            current_time = time.time()
            if current_time - last_beep_time > beep_interval:
                beep(int(freq), 150)
                last_beep_time = current_time

            # Mostra apenas o número do grupo detectado
            texto = f"Grupo: {closest_index}"
            cv2.putText(frame, texto, (x - 60, y - r - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Sistema para Pessoas Cegas - Identificação de Tampinhas", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
        break

cap.release()
cv2.destroyAllWindows()
