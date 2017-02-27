from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from sqlalchemy import func
from collections import OrderedDict
import os
import numpy as np
import urllib.request
from nameparser import HumanName

from app import app, db
from models import Book, NewBook

from schemas import ma, book_schema, books_schema
from .forms import LoginForm
# goodreads imports
from goodreads import client
from apikey import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from rauth.service import OAuth1Service, OAuth1Session


#-------------------------------------------------------------------------
# View entire library
#-------------------------------------------------------------------------
@app.route('/')
@app.route('/library')
def view_library():
    books = Book.query.order_by(Book.Author_lname,
                                Book.Author_fname,
                                Book.Title).all()
    return(render_template('table.html', books=books))

@app.route('/sort=<var>')
def sortByVar(var):
    
    if var == 'Author': var = 'Author_lname'

    # define sort order -- passed in var is the primary
    sort_order = np.array([var, 'Author_lname', 'Author_fname', 'Title'])
    _, idx = np.unique(sort_order, return_index=True)
    sort_order = sort_order[np.sort(idx)]

    if np.size(sort_order) == 3: # when sorting by author or title
        res = Book.query.order_by(sort_order[0], sort_order[1], sort_order[2]).all()    
    elif np.size(sort_order) == 4:
        res = Book.query.order_by(sort_order[0], sort_order[1], sort_order[2], sort_order[3]).all()    

    return(render_template('table.html', books=res))

#-------------------------------------------------------------------------
# View each book
#-------------------------------------------------------------------------
@app.route('/library/isbn=<query>')
def view_eachBook(query):
    book = Book.query.filter( Book.ISBN == query ).first()

    # convert object to dictionary!
    #book_dict = OrderedDict((col, getattr(res, col)) for col in res.__table__.columns.keys())

    return(render_template('book.html', book=book))

#-------------------------------------------------------------------------
# Search
#-------------------------------------------------------------------------
@app.route('/search')
def searchByVar():

    kwargs = request.args.to_dict()
    
    if 'Author' in kwargs:
        kwargs['Author_lname'] = kwargs.pop('Author')
        kwargs['Author_lname'] = HumanName(kwargs['Author_lname']).last
    
    # define sort order -- passed in var is the primary
    sort_order = np.array(['Author_lname', 'Author_fname', 'Title'])
    _, idx = np.unique(sort_order, return_index=True)
    sort_order = sort_order[np.sort(idx)]

    if np.size(sort_order) == 3: # when sorting by author or title
        books = Book.query.filter_by(**kwargs).order_by(sort_order[0], sort_order[1], sort_order[2]).all()    
    elif np.size(sort_order) == 4:
        books = Book.query.filter_by(**kwargs).order_by(sort_order[0], sort_order[1], sort_order[2], sort_order[3]).all()    

    return(render_template('table.html', books=books))
    
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
        
        flash('%s by %s Added' %(form.Title.data, form.Author.data))
        return(redirect(url_for('view_library')))

    return(render_template('register.html', form=form))


@app.route("/delete", methods=["DELETE"])
def delete(isbn):
    res = Book.query.get_or_404(isbn)
    
    db.session.delete(res)
    db.session.commit()
    
    return jsonify({"message": "Book Deleted"})


#-------------------------------------------------------------------------
# Fetch metadata from Goodreads
#-------------------------------------------------------------------------
@app.route('/fetch?isbn=<isbn>', methods=['GET', 'POST'])
def fetch_goodreads(isbn):
    
    session = OAuth1Session(
        consumer_key = CONSUMER_KEY,
        consumer_secret = CONSUMER_SECRET,
        access_token = ACCESS_TOKEN,
        access_token_secret = ACCESS_TOKEN_SECRET
    )

    gc = client.GoodreadsClient(session.consumer_key, session.consumer_secret)

    gc.authenticate(session.access_token, session.access_token_secret)

    if isbn:     
        # grab the  GoodreadsBook instance
        book = gc.book(isbn = isbn)

        # diwnload cover image if it does not exist
        path = 'app/static/coverImages/'
        fname = ''.join([isbn, '.jpg'])
        if not os.path.isfile( ''.join([path, fname]) ):
            urllib.request.urlretrieve( book._book_dict.get('image_url', ''), ''.join([path, fname]) )

        # create a new book instance
        newBook = Book(ISBN = isbn,
                       Title = book._book_dict.get('title', 'None'),
                       Author = HumanName(book.authors[0].name),
                       Language = book._book_dict.get('language_code', ''),
                       image_url = fname,
                       Publisher = book.publisher,
                       Published = book.publication_date)
    else:
        raise GoodreadsClientException("book id or isbn required")

    # convert object to dictionary!
    book_dict = OrderedDict((col, getattr(newBook, col)) for col in newBook.__table__.columns.keys())

    return(render_template('book.html', book_dict=book_dict))
 
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
