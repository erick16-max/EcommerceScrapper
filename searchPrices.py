
from bs4 import BeautifulSoup
import requests
import re

search_term = input ("What product are you looking for:")
url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, 'html.parser')

page_text = doc.find(class_="list-tool-pagination-text")
pages = int(str(page_text).split('/')[-3][-2])

items_found = {}
for page in range(1, pages + 1):
    url = f"https://www.newegg.ca/p/pl?d={search_term}&{page}=4"
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')
    items_div = doc.find(class_= "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = items_div.find_all(text =re.compile(search_term))

    for item in items:
        parent_link = item.parent
        if parent_link.name != "a":
            continue
        link = parent_link['href']
        container_parent =parent_link.parent.parent
        price = container_parent.find(class_= "price-current").strong.string
        items_found[item] = {'price':int(price.replace(",","")),'item_link':link}
        print(items_found)

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(item[1]['price'])
    print(item[1]['item_link'])

       


