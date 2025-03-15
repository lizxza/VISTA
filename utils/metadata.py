# metadata.py
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

METADATA_FILE = "metadata.xml"

def save_metadata(image_path, objects, text):
    # Путь к общему файлу метаданных
    metadata_path = os.path.join(os.path.dirname(image_path), METADATA_FILE)
    
    # Создаем или загружаем существующий XML
    if os.path.exists(metadata_path):
        tree = ET.parse(metadata_path)
        root = tree.getroot()
    else:
        root = ET.Element('metadata')
        tree = ET.ElementTree(root)

    # Уникальное имя изображения (без расширения)
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Удаляем старую запись, если существует
    for image_elem in root.findall(f"image[@name='{base_name}']"):
        root.remove(image_elem)

    # Создаем новую запись
    image_elem = ET.SubElement(root, 'image', name=base_name)
    
    # Добавляем объекты
    for obj in objects:
        obj_elem = ET.SubElement(image_elem, 'object')
        obj_elem.text = obj.split(' (')[0]  # Убираем confidence
    
    # Добавляем текст
    text_elem = ET.SubElement(image_elem, 'text')
    text_elem.text = text if text else ""  # Пустая строка, если текста нет

    # Форматируем XML с правильными отступами
    xml_str = ET.tostring(root, encoding='utf-8', method='xml')
    xml_pretty = minidom.parseString(xml_str).toprettyxml(indent="\t", encoding='utf-8')

    # Убираем лишние пустые строки, добавленные minidom
    xml_pretty = b"\n".join([line for line in xml_pretty.splitlines() if line.strip()])

    # Сохраняем файл
    with open(metadata_path, 'wb') as f:
        f.write(xml_pretty)