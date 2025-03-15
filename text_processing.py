import easyocr
from pyaspeller import YandexSpeller

reader = easyocr.Reader(['ru', 'en'])
speller = YandexSpeller()

def extract_and_correct_text(image_path):
    # Распознавание текста
    results = reader.readtext(image_path, detail=0)
    raw_text = ' '.join(results)
    # Исправление опечаток
    corrected_text = speller.spelled(raw_text)
    return corrected_text
