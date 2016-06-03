from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from sqlalchemy import func
from collections import OrderedDict

from app import app
from models import db, Book, NewBook
from schemas import ma, book_schema, books_schema
from .forms import LoginForm

#-------------------------------------------------------------------------
# View entire library
#-------------------------------------------------------------------------
@app.route('/')
@app.route('/library')
def view_library():
    res = Book.query.order_by(Book.Author_LastName, Book.Author_FirstName, Book.Title).all()
    return(render_template('table.html', books=res))

@app.route('/library/by-title/')
def view_byTitle():   
    res = Book.query.order_by(Book.Title, Book.Author_LastName, Book.Author_FirstName).all()
    return(render_template('table.html', books=res))

@app.route('/library/by-author/')
def view_byAuthor():   
    res = Book.query.order_by(Book.Author_LastName, Book.Author_FirstName, Book.Title).all()
    return(render_template('table.html', books=res))

@app.route('/library/by-genre/')
def view_byGenre():   
    res = Book.query.order_by(Book.Genre, Book.Title, Book.Author_LastName, Book.Author_FirstName).all()
    return(render_template('table.html', books=res))

@app.route('/library/by-read/')
def view_byRead():   
    res = Book.query.order_by(Book.Read, Book.Title, Book.Author_LastName, Book.Author_FirstName).all()
    return(render_template('table.html', books=res, sort_on='Title'))

#-------------------------------------------------------------------------
# View each book
#-------------------------------------------------------------------------
@app.route('/library/view/<query>')
def view_eachBook(query):
    res = Book.query.filter( Book.ISBN == query ).first()

    # convert object to dictionary!
    book_dict = OrderedDict((col, getattr(res, col)) for col in res.__table__.columns.keys())

    return(render_template('book.html', book_dict=book_dict))

#-------------------------------------------------------------------------
# Search by different fields
#-------------------------------------------------------------------------
@app.route('/by-author/<query>')
def searchByAuthor(query):
    res = Book.query.filter( func.lower(Book.Author_LastName) == func.lower(query) ).order_by(Book.Author_FirstName, Book.Title).all()
    return(render_template('table.html', books=res))

@app.route('/by-title/<query>')
def searchByTitle(query):
    res = Book.query.filter( func.lower(Book.Title) == func.lower(query) ).order_by(Book.Author_LastName, Book.Author_FirstName,).all()
    return(render_template('table.html', books=res))

@app.route('/by-genre/<query>')
def searchByGenre(query):
    res = Book.query.filter( func.lower(Book.Genre) == func.lower(query) ).order_by(Book.Author_LastName, Book.Author_FirstName, Book.Title).all()
    return(render_template('table.html', books=res))

@app.route('/by-read/<query>')
def searchByRead(query):
    res = Book.query.filter( func.lower(Book.Read) == func.lower(query) ).order_by(Book.Author_LastName, Book.Author_FirstName, Book.Title).all()
    return(render_template('table.html', books=res))

#-------------------------------------------------------------------------
# Create / delete / edit entries
#-------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = NewBook(request.form)
    
    if request.method == 'POST' and form.validate():
        book = book_schema.load(request.form)
    
        db.session.add(book)
        db.session.commit()
        
        flash('%s by %s Added' %(form.Title.data, form.Author_LastName.data))
        return(redirect(url_for('view_library')))

    return(render_template('register.html', form=form))


@app.route("/books/<isbn>", methods=["DELETE"])
def delete_book(ISBN):
    res = Book.query.get_or_404(ISBN)
    db.session.delete(res)
    db.session.commit()
    
    return jsonify({"message": "Book Deleted"})

#-------------------------------------------------------------------------
# Error Handlers
#-------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(error):
    resp = jsonify({"error": "not found"})
    resp.status_code = 404
    return(resp)

@app.errorhandler(401)
def unauthorized(error):
    resp = jsonify({"error": "Unauthorized"})
    resp.status_code = 401
    return(resp)

#-------------------------------------------------------------------------
# Login form
#-------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST', 'ADD', 'DELETE'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return(redirect('/library'))
    return(render_template('login.html', 
                           title='Sign In',
                           form=form))
