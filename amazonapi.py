from flask import Flask,jsonify
from selectorlib import Extractor
import requests
import json
from time import sleep

e = Extractor.from_yaml_file('search_results.yml')


app= Flask(__name__)
@app.route("/result/<int:price>",methods=["GET"])
def result(price):
    return jsonify(code(price))


def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None

    return e.extract(r.text)

def code(price):
    price=str(price)
    for url in ["https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A16225009011%2Cp_36%3A"+price+"00-"+price+"00&dc&qid=*&rnid=*&ref=*"]:
        data = scrape(url) 
        if data:
            for product in data['products']:
                if product["price1"]=='$'+price+'.00' or product["price"]=='$'+price+'.00':
                    return(product)
        
if __name__=="__main__":
    app.run(debug=True,use_reloader=False)
