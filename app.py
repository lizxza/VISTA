from flask import Flask, render_template, request, send_from_directory, send_file
import os
from werkzeug.utils import secure_filename
from models.object_detection import detect_objects
from models.text_processing import extract_and_correct_text
from utils.metadata import save_metadata
from utils.database import ImageDB


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = ImageDB()

# Новый роут для доступа к метаданным
@app.route('/metadata/<filename>')
def get_metadata(filename):
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], 'metadata', f"{os.path.splitext(filename)[0]}.xml")
    return send_file(metadata_path, mimetype='text/xml')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']


        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Обнаружение объектов
            objects, processed_path = detect_objects(filepath)
            # Распознавание текста
            text = extract_and_correct_text(filepath)
            # Сохранение метаданных
            save_metadata(filepath, objects, text)
            # Добавление в базу данных
            db.add_image(filename, objects, text)
            
            return render_template('results.html', 
                      filename=os.path.basename(processed_path),
                      objects=objects, 
                      text=text)
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query')
        if not query:
            raise ValueError("Пустой запрос")
        results = db.search_images(query)
        return render_template('search.html', results=results)
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        return render_template('search.html', results=None)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
