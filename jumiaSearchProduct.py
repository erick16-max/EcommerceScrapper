from itertools import count
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

#making chrome headless--No chrome browser UI launched
options = Options()
#options.add_argument("--headless")

#getting Data from jumia Site
def jumiaData():
    jumia_data_list = []
    search_item = input('Search for the product:') 
    search_product = search_item.lower()

    ser = Service("C:\src\BrowserDrivers\ChromeDriver\chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=options)

    #getting the Jumia url to render dynamic data using Selenium
    URL = f'https://www.jumia.co.ke/catalog/?q={search_product}'
    driver.get(URL)
    html = driver.page_source

    #parsing the data into Html using Beautiful soup
    soup = BeautifulSoup(html, 'html.parser')
    card_body = soup.find(class_='-paxs row _no-g _4cl-3cm-shs')

    #The products have no pagination
    if card_body.next_sibling is None:
        page_url = f'https://www.jumia.co.ke/catalog/?q={search_product}'
        driver.get(page_url)
        html = driver.page_source
        #parsing the data into Html
        soup = BeautifulSoup(html, 'html.parser')
        product_container = soup.find(class_='-paxs row _no-g _4cl-3cm-shs')
        products = product_container.find_all('article', {'class':'prd _fb col c-prd'})
        #finding the each product
        for product in products:
            product_href = product.find('a',href=True)['href']
            product_link = f'https://www.jumia.co.ke{product_href}'
            product_name = product.find(class_='info').h3.string
            product_price =product.find(class_='info').find(class_='prc').string
            product_name = str(product_name)
            #Removing the Ksh and turning price to Int for sorting :)
            product_price = list(str(product_price))
            del product_price[0:4]
            price =''.join(str(item) for item in product_price)
            product_price =int(price.replace(',',''))
            
            #the product has all the three items 
            if product_price and product_price and product_link:
              

                product_found = {
                        'product_name':product_name,
                        'product_price':product_price,
                        'product_link' : product_link
                }
                #print(product_found)
            else:
                product_found = {}

            jumia_data_list.append(product_found)

    else:
        page_links_pagination = soup.find(class_='pg-w -ptm -pbxl')
        page_links = page_links_pagination.find('a', {'aria-label':'Last Page','class':'pg'}, href= True)['href']
        pages =int(page_links.split('=')[-1][:2])
        
        for page in range(1, pages+1):
            
            page_url = f'https://www.jumia.co.ke/catalog/?q={search_product}&page={page}#catalog-listing'
            print(page_url)
            driver.get(page_url)
            html = driver.page_source
            #parsing the data into Html
            soup = BeautifulSoup(html, 'html.parser')
            product_container = soup.find(class_='-paxs row _no-g _4cl-3cm-shs')
            products = product_container.find_all('article', {'class':'prd _fb col c-prd'})

            #finding the each product
        for product in products:
            product_href = product.find('a',href=True)['href']
            product_link = f'https://www.jumia.co.ke{product_href}'
            product_name = product.find(class_='info').h3.string
            product_price =product.find(class_='info').find(class_='prc').string
            product_name = str(product_name)
            #Removing the Ksh and turning price to Int for sorting :)
            product_price = list(str(product_price))
            del product_price[0:4]
            price =''.join(str(item) for item in product_price)
            product_price =int(price.replace(',',''))
            
            #the product has all the three items 
            if product_price and product_price and product_link:
              

                product_found = {
                        'product_name':product_name,
                        'product_price':product_price,
                        'product_link' : product_link
                }
                #print(product_found)
            else:
                product_found = {}

            jumia_data_list.append(product_found)

    driver.quit()
    #sorting the product using the price
    jumia_sorted_products = sorted(jumia_data_list, key=lambda x:x['product_price'])
                
    print (jumia_sorted_products)

        
        
jumiaData()
    
       
  
        


    

    
    


    