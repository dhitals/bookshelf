#!/Users/saurav/Envs/flask/bin/python
from app import app, views
import sys
from config import SQLALCHEMY_DATABASE_URI
from models import db, Book
from db_importCSV import db_importCSV
from sqlalchemy import create_engine

if __name__ == "__main__":
    if "createdb" in sys.argv:
        with app.app_context():
            df = db_importCSV('data/books.csv')
            engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
            df.to_sql('books', engine, flavor='sqlite', if_exists='replace')
        print('Database Created!')
        
    elif "seeddb" in sys.argv:
        with app.app_context():
            b1 = Book(ISBN="1", Title= "Lord of the Rings", Author= "Tolkien, J. R. R.")            
            db.session.add_all([b1])
            db.session.commit()
        print("Database seeded!")
        
    else:            
        app.run(debug=True)
