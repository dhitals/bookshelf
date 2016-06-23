""" 
Fetch cover images for all books in the existing library -- 
meant for one-time usage
 """

import numpy as np
import os
import urllib.request
from db_importCSV import db_importCSV
# goodreads imports
from goodreads import client
from goodreads.request import GoodreadsRequestException
from apikey import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from rauth.service import OAuth1Service, OAuth1Session

def fetch_cover_image(isbns):
    
    session = OAuth1Session(
        consumer_key = CONSUMER_KEY,
        consumer_secret = CONSUMER_SECRET,
        access_token = ACCESS_TOKEN,
        access_token_secret = ACCESS_TOKEN_SECRET
    )

    gc = client.GoodreadsClient(session.consumer_key, session.consumer_secret)

    gc.authenticate(session.access_token, session.access_token_secret)

    for isbn in isbns:

        # download cover image if it does not exist
        path = 'app/static/'
        fname = ''.join(['coverImages/', str(isbn), '.jpg'])
        if not os.path.isfile( ''.join([path, fname]) ):
            # grab the  GoodreadsBook instance
            try:
                book = gc.book(isbn = isbn)

                print('Importing cover for %s' %isbn)
                urllib.request.urlretrieve( book._book_dict.get('image_url', ''), ''.join([path, fname]) )
            except (GoodreadsRequestException):
                print('Could not import %s. ISBN %s not found in Goodreads.' %(isbn, isbn))
                

    return


df = db_importCSV('data/books.csv')
# get cover images only if len(ISBN) == 13
isbns = [ x for x in df.ISBN if len(str(x)) == 13]

fetch_cover_image(isbns)
