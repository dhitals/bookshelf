from app import db
from sqlalchemy.orm import class_mapper, ColumnProperty
from flask_login import UserMixin
from wtforms import Form as WTForm, BooleanField, DateField, SelectField, IntegerField, StringField, validators

# create a Book subclass
class Book(db.Model):
    __tablename__ = 'books'
    
    ISBN = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64), nullable=False) 
    Author_LastName = db.Column(db.String(32), nullable=False)
    Author_FirstName = db.Column(db.String(32), nullable=True) 
    Original_Language = db.Column(db.String(32), nullable=True)
    Translator = db.Column(db.String(32), nullable=True)
    First_Published = db.Column(db.String(32), nullable=True)
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
        return('<Book - %s: %s - %s>' % (self.ISBN, self.Title, self.Author_LastName))
    
    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return([prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)])

class NewBook(WTForm):
    ISBN = StringField('ISBN', [validators.Length(min=13, max=13, message='ISBN must be 13 digits long.')])
    Title = StringField('Title', [validators.Length(min=2)])
    Author_LastName = StringField('Author Last Name', [validators.Length(min=2)])
    Author_FirstName = StringField('Author First Name', [validators.Length(min=1)]) 
    Original_Language = StringField('Original Language')
    Translator = StringField('Translator')
    First_Published = DateField('First Published', format='%y')
    Series = StringField('Series')
    SeriesIndex = StringField('Series Index')
    Genre = StringField('Genre')
    Collection = StringField('Collection')
    Format = SelectField('Format', choices=[(0, 'Paperback'), (1, 'Hardback'), (2, 'eBook'), (3, 'Audio Book')])
    Read = SelectField('Read', choices=[(0, 'Read'), (1, 'Unread')])
    Rating = IntegerField('Rating')
    Status = SelectField('Status', choices=[(0, 'Owned'), (1, 'Borrowed'), (2,'Wanted'), (3, 'Lent Out')])
    LentOutTo = StringField('Lent Out To')
    CoverImage = StringField('Cover Image')

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    #api_key = db.Column(db.String(64), unique=True, index=True)
