import requests 
from bs4 import BeautifulSoup
import sqlite3

def pars(soup, data):  
    product_info = soup.find_all(class_="product--info")
    for element in product_info:
        links =element.find(class_="product--title").get('href')
        brand = element.find(class_="listing--supplier-link cultizm-supplier-name").text
        name = element.find(class_="product--title").text
        try:
            price = element.find(class_="price--default is--nowrap").text
            price_discont = "-"
        except Exception:
            price_discont = element.find(class_="price--default is--nowrap is--discount").text
            price = element.find(class_="price--discount is--nowrap").text       
        response = requests.get(url=links)
        foot_ex = BeautifulSoup(response.text, 'lxml')
        item_code = foot_ex.find('li', class_="base-info--entry entry--suppliernumber").find(class_="entry--content").text
        style_foot = foot_ex.find('div', class_="product--description").text.split("Style:")
        style_foot.pop(0)   
        index_s = str(style_foot).index("- Color:")
        style_foot =str(style_foot)[2:index_s]
        style_foot = style_foot.replace("\\xa0", '')    
        stroka = (item_code, name, brand, style_foot, price, price_discont, links)
        data.append(stroka)
        
def createDB(data):
    conn = sqlite3.connect('/home/pavlo/pavlik/python/bot_for_IOri/chromedriver/pars_foots.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS cultizm(
        Item_Code TEXT,
        Name TEXT,
        Brand TEXT,
        Style_Foot TEXT,
        Price TEXT,
        Price_Discont TEXT,
        Link TEXT);
    """)
    conn.commit()
    conn.executemany("INSERT INTO cultizm(Item_Code, Name, Brand, Style_Foot, Price, Price_Discont, Link) VALUES(?, ?, ?, ?, ?, ?, ?);", data)
    conn.commit()
    conn.close()

def find_max_pages(url):
    soup = crete_request(url)
    count_page_max = int(soup.find(class_="paging--display").find('strong').text)
    return count_page_max

def crete_request(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def main():
    data = []
    url = "https://www.cultizm.com/us/widgets/listing/listingCount/sCategory/468?p=1&boxAnchor=SW61153&c=468&o=1&n=108&loadProducts=1"
    count_page_max = find_max_pages(url)
    counter = 1
    for count_page in range(1, count_page_max+1):
        url = "https://www.cultizm.com/us/widgets/listing/listingCount/sCategory/468?p="+str(count_page)+"&boxAnchor=SW61153&c=468&o=1&n=108&loadProducts=1"
        soup = crete_request(url)
        pars(soup, data)
        print(counter," - page: Successfully")
        counter+=1
    createDB(data)
    
if __name__ == '__main__':
    main()




