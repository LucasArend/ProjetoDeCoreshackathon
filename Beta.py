import cv2
import numpy as np
from skimage import color

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

color_groups_names = [
    "Preto", "Vermelho", "Laranja", "Amarelo",
    "Verde", "Azul", "Roxo", "Branco"
]

# Converte BGR para LAB
color_groups_lab = np.array([
    color.rgb2lab(np.array([[list(reversed(c))]], dtype=np.uint8) / 255.0)[0, 0]
    for c in color_groups_bgr
])

def color_distance_lab(c1, c2):
    return np.linalg.norm(c1 - c2)

# Captura da câmera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_original = frame.copy()
    gray = cv2.cvtColor(frame_original, cv2.COLOR_BGR2GRAY)

    # Detecta círculos (tampinhas)
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
        param1=100, param2=30, minRadius=20, maxRadius=80
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x, y, r) in circles[0, :1]:  # Só o primeiro círculo
            # Desenha o círculo detectado
            cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

            # Máscara circular para região da tampinha
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)

            # Média da cor na área da tampinha (LAB)
            mean_bgr = cv2.mean(frame_original, mask=mask)[:3]
            mean_lab = color.rgb2lab(
                np.array([[list(reversed(mean_bgr))]], dtype=np.uint8) / 255.0
            )[0, 0]

            # Compara com as cores da paleta
            distances = [color_distance_lab(mean_lab, c) for c in color_groups_lab]
            closest_index = int(np.argmin(distances))
            nome_cor = color_groups_names[closest_index]

            # Mostra o nome da cor na imagem
            cv2.putText(frame, f"Cor: {nome_cor}", (x - 40, y - r - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Detecção de Cor da Tampinha", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
