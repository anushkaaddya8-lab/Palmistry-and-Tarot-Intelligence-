from ultralytics import YOLO
import cv2
import os
from pathlib import Path


# ==========================================
# YOLO PALM LINE DETECTION
# ==========================================

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Trained YOLO model
MODEL_PATH = (
    PROJECT_ROOT
    / "runs"
    / "detect"
    / "train"
    / "weights"
    / "best.pt"
)

# Load trained model
model = YOLO(str(MODEL_PATH))


def detect_palm_lines(image_path, output_folder):

    # --------------------------------------
    # 1. Check image
    # --------------------------------------
    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # --------------------------------------
    # 2. Create output folder
    # --------------------------------------
    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # --------------------------------------
    # 3. YOLO prediction
    # --------------------------------------
    results = model.predict(
        source=image_path,
        conf=0.25,
        imgsz=640,
        save=False
    )

    result = results[0]

    # --------------------------------------
    # 4. Create annotated image
    # --------------------------------------
    annotated_image = result.plot()

    output_path = os.path.join(
        output_folder,
        "detected_palm_lines.jpg"
    )

    cv2.imwrite(
        output_path,
        annotated_image
    )

    # --------------------------------------
    # 5. Extract detected classes
    # --------------------------------------
    detections = []

    if result.boxes is not None:

        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )

            class_name = model.names[
                class_id
            ]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            detections.append({
                "class": class_name,
                "confidence": round(
                    confidence,
                    3
                ),
                "box": {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                }
            })

    # --------------------------------------
    # 6. Print results
    # --------------------------------------
    print(
        "Palm line detection completed."
    )

    print(
        "Detected lines:"
    )

    for detection in detections:
        print(
            f"{detection['class']} "
            f"({detection['confidence']})"
        )

    print(
        f"Output saved to: {output_path}"
    )

    # --------------------------------------
    # 7. Return result
    # --------------------------------------
    return {
        "detections": detections,
        "output_image": output_path
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    image_path = (
        PROJECT_ROOT
        / "datasets"
        / "palmistry"
        / "001"
        / "001_F_L_32.JPG"
    )

    output_folder = (
        PROJECT_ROOT
        / "datasets"
        / "palmistry"
        / "processed"
    )

    result = detect_palm_lines(
        str(image_path),
        str(output_folder)
    )

    print(result)