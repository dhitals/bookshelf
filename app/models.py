from app import db

# create a Book subclass
class Book(db.Model):
    __tablename__ = 'books'
    
    ISBN = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64), nullable=False) 
    Author = db.Column(db.String(32), nullable=False) 
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
        """"""
        return('<Book - %s: %s - %s>' % (self.ISBN, self.Title, self.Author))