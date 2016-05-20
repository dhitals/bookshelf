import pandas as pd

# returns a pandas df from a csv file
def db_importCSV(fname):
    df = pd.read_csv(fname)

    # modify the df so that datatypes are as desired 
    df = df.drop(['Location', 'Price', 'Comment', 'Loan/Borrow'], 1)
    df.ISBN = df.ISBN.fillna(0).astype(int)
    df.Status = df.Status.fillna('0') # Owned, Wanted, Loaned
    df.Read = df.Read.fillna(0).astype('bool')
    df.Format = df.Format.fillna('') # paperback, hardback, ebook
    df.SeriesIndex = df.SeriesIndex.fillna('')
    # new columns
    df['CoverImage'] = ''
    df['Collection'] = ''
    df['LentOutTo']  = ''

    # rearrange a couple of the columns
    cols = df.columns.tolist()
    cols.insert(4, cols.pop(cols.index('Read')))
    cols.insert(-1, cols.pop(cols.index('Status')))
    cols.insert(-1, cols.pop(cols.index('Format')))

    df = df[cols]
    
    return(df)