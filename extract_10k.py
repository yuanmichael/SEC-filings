# GOAL: Build a program which (1) takes a ticker, (2), returns the CIK, (3) grabs the XBRL data containing all the financials
# NOTE: Should limit to just the 10-Ks? 

import requests
from collections import defaultdict, Counter



# use the SEC's .txt file to convert any ticker to its corresponding CIK
def grab_cik(ticker: str) -> int:
    # converts input to lower case, since the SEC's .txt file is all in lower case
    ticker = ticker.lower()
    response = requests.get("https://www.sec.gov/include/ticker.txt", headers={"User-Agent": "Michael (test@test.com)"})
    
    # grabs the response, and splits it based on each new line ('\n\')
    response_list: list = response.text.split('\n')
    dict = {}

    for line in response_list:
        # split each item based on the '/t' thing 
        data = line.split('\t')

        # now we've split each data into 2 parts. the ticker + the cik 
        key, value = data
        dict[key] = int(value)

    cik = dict[ticker]
    print(f"{ticker} : {cik}")
    return cik
    

def grab_xbrl(cik: int):
    # web scraping setup
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{str(cik).zfill(10)}.json"
    headers = {"User-Agent": "Michael (test@test.com)"}
    session = requests.Session() 
    
    # grab the JSON content under the key "us-gaap"
    gaap_data = session.get(url, headers=headers).json()["facts"]["us-gaap"]
#    counter = 0
#    for key, value in gaap_data.items():
#        counter += 1
#        print(key, value)
#        if counter == 10:
#            break

    # intitializes a dict. Its values are nested dictionaries. And those values are lists of other dictionaries 
    financials_dict = defaultdict(lambda: defaultdict(list))

    # loop through the JSON content after "us-gaap" and append relevant values to a dictionary
    for metric, details in gaap_data.items():
        data = details.get("units")
        data = data.get("USD")
        if data: 
            for item in data:
                value = item["val"]
                
                # TODO: Sometimes, FY2023 has multiple values. E.g. 2021, 2022, and 2023 all called "FY2023". Should fix
                # in example, he used the "accn" field to filter for the most recent 10-K 

                # grab data fields under each respective key. Remember to use .get() because some may not exist 
                fy = item.get("fy")
                fp = item.get("fp")
                form = item.get("form")
                start = item.get("start")
                end = item.get("end")
                frame = item.get("frame")
                period = str(fy) + fp 

                # only accept 10-Ks
                if form != "10-K":
                    continue

                # append the period and value to the financials_dict                    
                financials_dict[metric][period].append(value) 

    # print function. Iterate through each key-value pair in financials_dict. Can't just print a dictionary   
    counter = 0
    for metric, periods in financials_dict.items():
        print(metric)
        for period, values in periods.items():
            print(f"{period}: {values}") 
        print()
        
        # only print the first 20 
        counter += 1
        if counter == 20:
            break
    
    return financials_dict



# INPUT the ticker here
def main():
    cik = grab_cik("abnb")
    financials_dict = grab_xbrl(cik)
    return financials_dict 


