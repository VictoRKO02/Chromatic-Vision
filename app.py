import cv2
import numpy as np
import os
from datetime import datetime

# RECONHECIMENTO DE CORES DE OBJETOS COM OPENCV
# Controles:
#   Q -> sair
#   S -> salvar frame atual
#
# O programa:
# 1. Captura imagem da webcam
# 2. Converte BGR -> HSV
# 3. Cria máscaras para diferentes cores
# 4. Encontra contornos
# 5. Exibe nome da cor, centro (x, y) e bounding box
# 6. Salva capturas na pasta "capturas"

MIN_AREA = 800

# Pasta onde os prints serão salvos
CAPTURE_FOLDER = "capturas"

# Cria a pasta automaticamente caso ela não exista
os.makedirs(CAPTURE_FOLDER, exist_ok=True)


# INTERVALOS DE CORES EM HSV

COLOR_RANGES = {
    "Vermelho": [
        (
            np.array([0, 100, 80]),
            np.array([10, 255, 255])
        ),
        (
            np.array([170, 100, 80]),
            np.array([179, 255, 255])
        ),
    ],

    "Laranja": [
        (
            np.array([11, 100, 80]),
            np.array([24, 255, 255])
        ),
    ],

    "Amarelo": [
        (
            np.array([25, 100, 80]),
            np.array([35, 255, 255])
        ),
    ],

    "Verde": [
        (
            np.array([36, 70, 60]),
            np.array([85, 255, 255])
        ),
    ],

    "Azul": [
        (
            np.array([86, 80, 60]),
            np.array([130, 255, 255])
        ),
    ],

    "Roxo": [
        (
            np.array([131, 60, 50]),
            np.array([169, 255, 255])
        ),
    ],
}

# CORES DAS CAIXAS NA TELA
# Formato BGR

DRAW_COLORS = {
    "Vermelho": (0, 0, 255),
    "Laranja": (0, 140, 255),
    "Amarelo": (0, 255, 255),
    "Verde": (0, 255, 0),
    "Azul": (255, 0, 0),
    "Roxo": (255, 0, 180),
}

# CRIAÇÃO DA MÁSCARA

def create_color_mask(hsv_frame, ranges):

    combined_mask = np.zeros(
        hsv_frame.shape[:2],
        dtype=np.uint8
    )

    for lower, upper in ranges:

        mask = cv2.inRange(
            hsv_frame,
            lower,
            upper
        )

        combined_mask = cv2.bitwise_or(
            combined_mask,
            mask
        )

    # Kernel para remoção de ruídos
    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    # Remove pequenos pontos
    combined_mask = cv2.morphologyEx(
        combined_mask,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )

    # Fecha pequenos buracos
    combined_mask = cv2.morphologyEx(
        combined_mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    return combined_mask

# DETECÇÃO DOS OBJETOS

def detect_objects(frame):

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )

    detections = []

    for color_name, ranges in COLOR_RANGES.items():

        mask = create_color_mask(
            hsv,
            ranges
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:

            area = cv2.contourArea(
                contour
            )

            # Ignora objetos muito pequenos
            if area < MIN_AREA:
                continue

            # Bounding box
            x, y, w, h = cv2.boundingRect(
                contour
            )

            # Centro do objeto
            center_x = x + w // 2
            center_y = y + h // 2

            detections.append(
                {
                    "cor": color_name,
                    "x": center_x,
                    "y": center_y,
                    "largura": w,
                    "altura": h,
                    "area": round(area, 2),
                }
            )

            draw_color = DRAW_COLORS[
                color_name
            ]

            # Desenha a caixa
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                draw_color,
                2
            )

            # Marca o centro
            cv2.circle(
                frame,
                (center_x, center_y),
                6,
                draw_color,
                -1
            )

            # Texto
            label = (
                f"{color_name} | "
                f"({center_x}, {center_y})"
            )

            cv2.putText(
                frame,
                label,
                (
                    x,
                    max(
                        y - 10,
                        25
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                draw_color,
                2,
                cv2.LINE_AA
            )

    return frame, detections


# SALVAR CAPTURA

def save_capture(frame):

    # Data e hora atual
    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    # Nome do arquivo
    filename = (
        f"captura_{timestamp}.jpg"
    )

    # Caminho completo
    filepath = os.path.join(
        CAPTURE_FOLDER,
        filename
    )

    # Salva a imagem
    success = cv2.imwrite(
        filepath,
        frame
    )

    if success:

        print(
            f"\nCaptura salva com sucesso:"
        )

        print(
            filepath
        )

    else:

        print(
            "\nErro ao salvar a captura."
        )


# PROGRAMA PRINCIPAL

def main():

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print(
            "Erro: não foi possível "
            "acessar a webcam."
        )

        print(
            "Verifique se outra aplicação "
            "está utilizando a câmera."
        )

        return

    # Resolução
    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )

    print("=" * 55)

    print(
        "RECONHECIMENTO DE CORES "
        "COM OPENCV"
    )

    print("=" * 55)

    print(
        "Q -> sair"
    )

    print(
        "S -> salvar captura"
    )

    print(
        f"Capturas serão salvas em: "
        f"{CAPTURE_FOLDER}/"
    )

    print("=" * 55)

    while True:

        success, frame = camera.read()

        if not success:

            print(
                "Erro ao capturar frame."
            )

            break

        # Espelha a imagem
        frame = cv2.flip(
            frame,
            1
        )

        # Detecta objetos
        processed_frame, detections = detect_objects(
            frame
        )

        # Exibe quantidade
        cv2.putText(
            processed_frame,
            (
                f"Objetos detectados: "
                f"{len(detections)}"
            ),
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Exibe instrução
        cv2.putText(
            processed_frame,
            "S = Salvar | Q = Sair",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Janela
        cv2.imshow(
            "Reconhecimento de Cores",
            processed_frame
        )

        key = cv2.waitKey(1) & 0xFF

        # Sai do programa
        if key == ord("q"):

            break

        # Salva captura
        if key == ord("s"):

            save_capture(
                processed_frame
            )

    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()