""" 
Fetch cover images for all books in the existing library -- 
meant for one-time usage
 """

from db_importCSV import db_importCSV
import urllib.request

def fetch_goodreads(isbns):

    df = db_importCSV('data/books.csv')
    
    session = OAuth1Session(
        consumer_key = CONSUMER_KEY,
        consumer_secret = CONSUMER_SECRET,
        access_token = ACCESS_TOKEN,
        access_token_secret = ACCESS_TOKEN_SECRET
    )

    gc = client.GoodreadsClient(session.consumer_key, session.consumer_secret)

    gc.authenticate(session.access_token, session.access_token_secret)

    for isbn in df.ISBN:
        print(isbn)
        # grab the  GoodreadsBook instance
        book = gc.book(isbn = isbn)

        # download cover image if it does not exist
        path = 'app/static/'
        fname = ''.join(['coverImages/', isbn, '.jpg'])
        if not os.path.isfile( ''.join([path, fname]) ):
            urllib.request.urlretrieve( book._book_dict.get('image_url', ''), ''.join([path, fname]) )

            """
    return
