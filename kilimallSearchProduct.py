from calendar import c
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


#making chrome headless--No chrome browser UI launched
options = Options()
#options.add_argument("--headless")



#getting Data from Kilimanl Site
def kilimallData ():
    kilimall_data_list =[]
    search_item = input('Search for the product:') 
    search_product = search_item.lower()

    #setting chrome as the web driver to use
    ser = Service("C:\src\BrowserDrivers\ChromeDriver\chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=options)

    #getting the kilimal url to render dynamic data
    URL = f'https://www.kilimall.co.ke/new/commoditysearch?q={search_product}'
    driver.get(URL)
    
    driver.implicitly_wait(10)
    html = driver.page_source

    #parsing the data into Html
    soup = BeautifulSoup(html, 'html.parser')

    #Getting total number of pages in the pagination
    pagination = soup.find(class_='leftpaging').span
    total_pages = str(pagination).split('/')[-2].split('<')[0]
    pages = int (total_pages)

    #initialoize empty product dict
    product_found = {}

    #Getting each page data
    for page in range(1, pages+1):
        URL = f'https://www.kilimall.co.ke/new/commoditysearch?q={search_product}&page={page}'
        driver.get(URL)
        
        #wait until products are located
        driver.implicitly_wait(10)

        #storing the rendered data 
        html = driver.page_source
        #parsing the data into Html
        soup = BeautifulSoup(html, 'html.parser')
        products_container = soup.find('section',{'class':'el-container containerbox is-vertical'}).find(class_='el-container')
        product_main = products_container.find('main',{'class':'el-main main-el'}).find(class_='imgbox')
        products= product_main.find_all(class_='el-col el-col-6')
        
        for product in products:
            product_item_name = product.find('div',{'class':'grid-content bg-purple clearfix'}).find(class_='wordwrap').div.string
            product_name= str(product_item_name)
            
            
            link =product.find('div',{'class':'grid-content bg-purple clearfix'}).find('a', href=True)['href']
            product_link = f'https://www.kilimall.co.ke{link}'
            #product_img_url = product.find('a').find(class_="imgClass").img['src']
            product_price = product.find(class_='wordwrap-box').find(class_="wordwrap-price").span.string
            #Removing the Ksh and turning price to Int for sorting :)
            product_price = list(str(product_price))
            del product_price[0:4]
            price =''.join(str(item) for item in product_price)
            product_price =int(price.replace(',',''))


            product_found = {
                    'product_name':product_name,
                    'product_price':product_price,
                    'product_link' : product_link
            }

                #print(product_found)
            
                
            kilimall_data_list.append(product_found)
    driver.quit()
    #sorting the product using the price
    kilimall_sorted_products = sorted(kilimall_data_list, key=lambda x:x['product_price'])
    print(kilimall_sorted_products)
            
            


    driver.quit()
       
        


    

kilimallData()
    
    


    

