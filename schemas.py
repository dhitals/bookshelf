from flask_marshmallow import Marshmallow
from models import User, Book

ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        model = User
        
        fields = ('id', 'name')
        
user_schema = UserSchema()


class BookSchema(ma.Schema):
    class Meta:
        model = Book
        
        fields = ('ISBN', 'Title', 'Author_lastName', 'Author_firstName', 'Genre', 'Read')

book_schema = BookSchema()
books_schema = BookSchema(many=True)
