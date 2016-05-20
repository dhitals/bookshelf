from flask import render_template
from app import app
from models import Book

@app.route('/')
#@app.route('/index')
def view_library():
    res = Book.query.all()
    return(render_template('eachBook.html', books=res))

@app.route('/by-author/')
def searchBy():
    res = Book.query.filter_by(Author='Adichie, Chimamanda Ngozi').all()
    return(render_template('eachBook.html', books=res))
