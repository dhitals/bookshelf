from flask_marshmallow import Marshmallow
from models import User, Book

ma = Marshmallow()
 
class BookSchema(ma.Schema):
    class Meta:
        model = Book
        
        fields = ('ISBN', 'Title', 'Author_LastName', 'Author_FirstName', 'Genre', 'Read')

book_schema = BookSchema()
books_schema = BookSchema(many=True)
