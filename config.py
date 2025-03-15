import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'}
SECRET_KEY = '5f4dcc3b5aa765d61d8327deb882cf99'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
