from flask_marshmallow import Marshmallow
from models import Book

ma = Marshmallow()
 
class BookSchema(ma.Schema):
    class Meta:
        model = Book
        
        fields = ('ISBN', 'Title', 'Author', 'Genre', 'Read')

book_schema = BookSchema()
books_schema = BookSchema(many=True)
