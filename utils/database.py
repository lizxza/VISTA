from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    objects = Column(String)
    text = Column(String)

class ImageDB:
    def __init__(self):
        self.engine = create_engine('sqlite:///images.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_image(self, filename, objects, text):
    	session = self.Session()
    	# Преобразуем список объектов в строку с разделителями
    	objects_str = ", ".join(objects) if objects else "Нет объектов"
    	text_str = text if text else "Нет текста"
    	image = Image(filename=filename, objects=objects_str, text=text_str)
    	session.add(image)
    	session.commit()
    	session.close()

    def search_images(self, query):
    	session = self.Session()
    	# Используем ilike для регистронезависимого поиска
    	search_pattern = f"%{query}%"
    	results = session.query(Image).filter(
        	(Image.objects.ilike(search_pattern)) | (Image.text.ilike(search_pattern))
    	).all()
		
    	session.close()
    	return results
