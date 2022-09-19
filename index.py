from bs4 import BeautifulSoup
import requests

url = "https://coinmarketcap.com/"

result = requests.get(url)

doc = BeautifulSoup(result.text, 'html.parser')

t_body = doc.tbody

trs = t_body.contents
prices = {}

def findPrices():
    for tr in trs[:10]:
        name, price = tr.contents[2:4]
        fixed_name =name.p.string
        fixed_price =price.span.string
        prices[fixed_name] = fixed_price
    return prices

print(findPrices())
        
    

    






