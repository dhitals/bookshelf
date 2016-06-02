from app import db
from sqlalchemy.orm import class_mapper, ColumnProperty
from flask_login import UserMixin
from wtforms import Form, BooleanField, StringField, validators

# create a Book subclass
class Book(db.Model):
    __tablename__ = 'books'
    
    ISBN = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64), nullable=False) 
    Author_lastName = db.Column(db.String(32), nullable=False)
    Author_firstName = db.Column(db.String(32), nullable=True) 
    Original_Language = db.Column(db.String(32), nullable=True)
    Translator = db.Column(db.String(32), nullable=True)
    Series = db.Column(db.String(32), nullable=True) 
    SeriesIndex = db.Column(db.SmallInteger, nullable=True) 
    Genre = db.Column(db.String(16), nullable=True) 
    Collection = db.Column(db.String(16), nullable=True) 
    Format = db.Column(db.String(16), nullable=True) 
    Read = db.Column(db.Boolean, nullable=True) 
    Rating = db.Column(db.Integer, nullable=True) 
    Status = db.Column(db.String(8), nullable=True)
    LentOutTo = db.Column(db.String(8), nullable=True) 
    CoverImage = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return('<Book - %s: %s - %s>' % (self.ISBN, self.Title, self.Author_lastName))
    
    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return([prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)])

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    #api_key = db.Column(db.String(64), unique=True, index=True)

class NewBook(Form):
    ISBN = StringField('ISBN', [validators.Length(min=13, max=13, message='ISBN must be 13 digits long.')])
    Title = StringField('Title', [validators.Length(min=2)])
    Author_lastName = StringField('Author_lastName', [validators.Length(min=2)]) 

