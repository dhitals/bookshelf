import pandas as pd
from nameparser import HumanName

# returns a pandas df from a csv file
def db_importCSV(fname):
    df = pd.read_csv(fname)

    # modify the df so that datatypes are as desired 
    df.ISBN = df.ISBN.fillna(0).astype(int)
    df.Status = df.Status.fillna('0') # Owned, Wanted, Loaned
    df.Read = df.Read.fillna(0).astype('bool')
    df.Format = df.Format.fillna('') # paperback, hardback, ebook
    df.SeriesIndex = df.SeriesIndex.fillna('')

    # store author last/first name for easier sorting
    # HumanName does not take lists :(
    df['Author_lname'] = [ HumanName(x).last for x in df.Author ]
    fname = [ HumanName(x).first  for x in df.Author ]
    mname = [ HumanName(x).middle for x in df.Author ]
    df['Author_fname'] = [ ''.join([x,y]) for x,y in zip(fname, mname) ]
    
    # new columns
    df['image_url'] = ''
    df['Collection'] = ''
    df['Lent_to']  = ''
    df['Language'] = ''
    df['Translator'] = ''
    df['Publication_Year'] = ''
    df['Publisher'] = ''    

    # drop unneccesarry cols
    df = df.drop(['Location', 'Price', 'Comment', 'Loan/Borrow'], 1)

    # rearrange a couple of the columns
    cols = df.columns.tolist()
    cols.insert(4, cols.pop(cols.index('Read')))
    cols.insert(-1, cols.pop(cols.index('Status')))
    cols.insert(-1, cols.pop(cols.index('Format')))

    df = df[cols]
    
    return(df)
