import argparse
import cv2
import numpy as np

MIN_AREA = 800

COLOR_RANGES = {
    "Vermelho": [
        (np.array([0, 100, 80]), np.array([10, 255, 255])),
        (np.array([170, 100, 80]), np.array([179, 255, 255])),
    ],
    "Laranja": [(np.array([11, 100, 80]), np.array([24, 255, 255]))],
    "Amarelo": [(np.array([25, 100, 80]), np.array([35, 255, 255]))],
    "Verde": [(np.array([36, 70, 60]), np.array([85, 255, 255]))],
    "Azul": [(np.array([86, 80, 60]), np.array([130, 255, 255]))],
    "Roxo": [(np.array([131, 60, 50]), np.array([169, 255, 255]))],
}

DRAW_COLORS = {
    "Vermelho": (0, 0, 255),
    "Laranja": (0, 140, 255),
    "Amarelo": (0, 255, 255),
    "Verde": (0, 255, 0),
    "Azul": (255, 0, 0),
    "Roxo": (255, 0, 180),
}


def create_mask(hsv, ranges):
    result = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for lower, upper in ranges:
        result = cv2.bitwise_or(result, cv2.inRange(hsv, lower, upper))

    kernel = np.ones((5, 5), np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel, iterations=2)

    return result


def process_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    detections = []

    for color_name, ranges in COLOR_RANGES.items():
        mask = create_mask(hsv, ranges)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            area = cv2.contourArea(contour)

            if area < MIN_AREA:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            cx = x + w // 2
            cy = y + h // 2

            detections.append({
                "cor": color_name,
                "centro": [cx, cy],
                "bbox": [x, y, w, h],
                "area": round(area, 2),
            })

            color = DRAW_COLORS[color_name]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.circle(image, (cx, cy), 5, color, -1)
            cv2.putText(
                image,
                f"{color_name} ({cx},{cy})",
                (x, max(20, y - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

    return image, detections


def main():
    parser = argparse.ArgumentParser(
        description="Reconhecimento de cores em uma imagem."
    )
    parser.add_argument("imagem", help="Caminho da imagem de entrada")
    parser.add_argument(
        "--saida",
        default="resultado.jpg",
        help="Caminho da imagem de saída"
    )

    args = parser.parse_args()

    image = cv2.imread(args.imagem)

    if image is None:
        raise FileNotFoundError(
            f"Nao foi possivel abrir a imagem: {args.imagem}"
        )

    result, detections = process_image(image)
    cv2.imwrite(args.saida, result)

    print("\nDeteccoes:")
    for item in detections:
        print(item)

    print(f"\nResultado salvo em: {args.saida}")


if __name__ == "__main__":
    main()
