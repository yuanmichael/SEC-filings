import requests
from collections import defaultdict
from collections import Counter
import time

url = "https://www.sec.gov/files/company_tickers_exchange.json"
headers = {"User-Agent": "Michael (test@test.com)"}
session = requests.Session() 

# define a class, Company, which stores the useful information we need for each company
class Company:
    def __init__(self, cik:int, name:str, ticker:str, exchange:str = None):
        self.cik = cik    
        self.name = name
        self.ticker = ticker
        self.exchange = exchange

# initializes the data. Calls to the SEC's endpoint in order to grab the first 4 fields under the "data" json header, for each respective company
def grab_companies() -> list[Company]:
    data = session.get(url, headers=headers).json()["data"]

    # initializes a list of Company objects (defined above), with 4 fields 
    companies = [
        Company(cik=field[0], name=field[1], ticker=field[2], exchange=field[3])
        for field in data
    ]

    return companies

# converts a list of Companies into a dictionary. Key is exchange and value is a list of Company info 
def group_by_exchange(companies: list) -> dict:
    acc_dict = defaultdict(list)

    for company in companies:
        acc_dict[company.exchange].append(company)
    return acc_dict

# TO DO: Grab the SIC for each company
def grab_sic(cik: int): 
    url = f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json"
    sicDescription = session.get(url, headers=headers).json()["sicDescription"]
    return sicDescription 



# MAIN FUNCTIONS BELOW

# function for sorting by exchange
def sort_by_exchange():
    # only grabs the first 500 companies from the SEC's endpoint
    companies = grab_companies()[:500] 
    # groups each company according to its exchange
    grouped = group_by_exchange(companies)

    # print out each key-value pair from above
    for exchange, companies in grouped.items():
        print(f"Exchange: {exchange}")
        for company in companies:
            # need to use "company.ticker", otherwise it just prints out the memory slot if it's just "ticker" 
            print(f"{company.ticker}")
        print()
 
 # Create a new dictionary with "key" as exchange and "value" as the number of companies within each exchange. 
    exchange_count = {exchange: len(companies) for exchange, companies in grouped.items()}
    print(exchange_count)

# function for sorting companies by industry (sic_descriptions)
def sort_by_industry():
    # need to limit to something small, like 20 companies, because of how long it takes to ping the endpoint for each CIK 
    companies = grab_companies()[:500]
    sic_list = []
    for company in companies:
        sic_list.append(grab_sic(company.cik))
        # wait 1 second before repeating the for loop
        #time.sleep(1) 
    
    # create a Dictionary: keys are the unique values of SICs, and values are the counts
    sorted_sics = Counter(sic_list)
    print(sorted_sics)

    return sorted_sics

#sort_by_exchange()
sort_by_industry()