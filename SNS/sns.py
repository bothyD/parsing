import undetected_chromedriver
from bs4 import BeautifulSoup
import sqlite3
import time

def pars(soup, data):   
    krosi = soup.find_all('article', class_='card product')
    for kros in krosi:
        item_code= kros.get('data-gtm-list-product').split(',')[1].split('"')[3]
        links ="https://www.sneakersnstuff.com" + kros.find('a', class_='card__link').get('href')
        brand = kros.find('span', class_='card__brand').contents[0]
        name = kros.find('strong', class_='card__name').contents[0]
        try:
            price = kros.find(class_="price__original").text
            price_discont = kros.find(class_="price__current").text.strip()
        except Exception:
            price=kros.find('span', class_='price__current').text.strip()
            price_discont = "-"
        stroka = (item_code, name, brand, price, price_discont, links)
        data.append(stroka)
        
def createDriver(url):
    try:
        driver = undetected_chromedriver.Chrome()
        driver.get(url=url)
        time.sleep(11)
        main_page = driver.page_source
        soup = BeautifulSoup(main_page, 'lxml')
        return soup
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def createDB(data):
    conn = sqlite3.connect('/home/pavlo/pavlik/python/bot_for_IOri/chromedriver/pars_foots.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS sns(
        Item_Code TEXT,
        Name TEXT,
        Brand TEXT,
        Price TEXT,
        Price_Discont TEXT,
        Link TEXT);
    """)
    conn.commit()
    conn.executemany("INSERT INTO sns(Item_Code, Name, Brand, Price, Price_Discont, Link) VALUES(?, ?, ?, ?, ?, ?);", data)
    conn.commit()
    conn.close()

def main():
    data = []
    count_page=1
    url = "https://www.sneakersnstuff.com/en/904/mens-sneakers/"+str(count_page)+"?orderBy=Popularity"  
    soup = createDriver(url)
    count_page_max =int(soup.find('span', class_='pagination__total').text)
    for count_page in range(1,count_page_max+1):
        url = "https://www.sneakersnstuff.com/en/904/mens-sneakers/"+str(count_page)+"?orderBy=Popularity"
        soup = createDriver(url)
        pars(soup, data)
    createDB(data=data)     
       
if __name__ == '__main__':
    main()
