import pandas as pd
import json

def get_data(link_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', outfile_name = 'US_stocks.json'):    
    stocks_available = pd.read_html(
        link_url)[0]
    # we can change this data to get any global Stock Market Exchange Data

    mapping = {}

    print(stocks_available)
    symbol = stocks_available['Symbol'].to_list()
    security = stocks_available['Security'].to_list()
    for idx in range(stocks_available.shape[0]):
        mapping[security[idx]] = symbol[idx]

    with open(outfile_name, "w") as outfile: 
        json.dump(mapping, outfile)



if __name__ == "__main__":
    get_data()