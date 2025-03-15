from ultralytics import YOLO
import cv2
import os
from transformers import pipeline
from functools import lru_cache

# Инициализация модели перевода для CPU
@lru_cache(maxsize=1000)
def get_translator():
    return pipeline(
        "translation_en_to_ru",
        model="Helsinki-NLP/opus-mt-en-ru",
        device=-1  # Принудительно используем CPU
    )

# Загрузка YOLO модели
model = YOLO('yolov8x.pt').to('cpu')  # Явное указание CPU

def translate_label(label_en: str) -> str:
    try:
        result = translator(label_en, max_length=40)
        return result[0]['translation_text'].lower()
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return label_en

def detect_objects(image_path):
    image = cv2.imread(image_path)
    
    # Отключение всех GPU-оптимизаций
    results = model(image, device='cpu')
    
    detections = []
    for result in results:
        annotated_image = result.plot()
        
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label_en = model.names[cls_id]
            label_ru = translate_label(label_en)
            confidence = round(float(box.conf[0]), 2)
            detections.append(f"{label_ru} ({confidence})")

    processed_path = os.path.join(
        os.path.dirname(image_path),
        f"processed_{os.path.basename(image_path)}"
    )
    cv2.imwrite(processed_path, annotated_image)

    return detections, processed_path

translator = get_translator()