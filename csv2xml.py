from pandas import read_csv
from feedgen.feed import FeedGenerator

# Validate xml file
# https://validator.w3.org/feed/check.cgi

def define_rss_header():
    """Set basic elements at the tome of xml file
    """
    fg = FeedGenerator()
    fg.id('http://lernfunk.de/media/654321')
    fg.title('Mustafa RSS project')
    fg.author( {'name':'Mustafa','email':'mustafadar338@gmail.com'} )
    fg.link( href='http://example.com', rel='alternate' )
    fg.logo('http://ex.com/logo.jpg')
    fg.subtitle('Mustafa cool feed!')
    fg.link( href='http://larskiesow.de/test.atom', rel='self' )
    fg.language('en')
    return fg

def load_data_from_csv(filename):        
    try:
        # load data using "|" as delimiter
        df = read_csv(filename, delimiter="|")
    except Exception as ex:
        print(f"Could not open {filename}. Reason: {str(ex)}")
        return None
        
    # convert columns to lowercase
    columns = [c.lower() for c in df.columns]
    df.columns = columns
    
    return df
        
def main():

    fg = define_rss_header()
    
    # Get the ATOM feed as string
    atomfeed = fg.atom_str(pretty=True) 
    
    # Get the RSS feed as string
    rssfeed  = fg.rss_str(pretty=True) 
    
    # Time to load data
    filename = 'quotes.csv'
    data = load_data_from_csv(filename)
    if data is None:
        print("Could not load data from csv file")
        return
    
    # Read each row from dataframe and
    # read value from the right column and set it
    # as a value for the current created xml entry
    for i in data.index:        
        # create XML entry (inside item section)
        fe = fg.add_entry()
        
        fe.id(f'http://lernfunk.de/media/654321/{i}')
        fe.title((
            f"<![CDATA[<h1>{data.at[i, 'source']} {data.at[i, 'dob-dod']}</h1>"
            f"<h3>{data.at[i, 'category']}</h3>]]>"
            
        ))
        fe.description(f"<![CDATA[<p><img width=\"50%\" src=\"{data.at[i, 'wpimg']}\"/></p>]]")
        fe.content(f"<![CDATA[<p>{data.at[i, 'quote']}</p>]]")
        fe.link(href=data.at[i, "wplink"])
        
    # Write the RSS feed to a file    
    fg.rss_file('rss.xml') 
        
if __name__ == '__main__':
    main()
