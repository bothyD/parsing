import undetected_chromedriver
from bs4 import BeautifulSoup
import sqlite3
import time

def pars(soup, data):
    krosi = soup.find_all('li', class_='item product product-item grid-col')
    for kros in krosi:
        
        product_info = kros.find(class_="product-card__info product details product-item-details")
        item_code= kros.find('div', class_="product-card__whislist wishlist-update").get('data-sku')        
        links = product_info.find('a', class_='set-product-storage').get('href')
        brand = product_info.find('a', class_='set-product-storage').text.strip()
        name = product_info.find('a', class_='product-item-link set-product-storage').text.strip()
        try:
            price_discont=product_info.find('span', class_='old-price sly-old-price no-display').find(class_="price").text.strip()
            price=product_info.find('span', class_='price-container price-final_price tax').find(class_="price").text.strip()
        except Exception:
            price_discont="-"
            price=product_info.find('span', class_='price-container price-final_price tax').find(class_="price").text.strip()
        stroka = (item_code, name, brand, price, price_discont, links)
        data.append(stroka)
        
def createDriver(url, count_page):
    try:
        driver = undetected_chromedriver.Chrome()
        driver.get(url=url)
        time.sleep(3)
        main_page = driver.page_source
        soup = BeautifulSoup(main_page, 'lxml')
        next_page = soup.find(class_="item pages-item-next next")
        print(count_page)    
        return soup, next_page
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        
def createDB(data):
    conn = sqlite3.connect('/home/pavlo/pavlik/python/bot_for_IOri/chromedriver/pars_foots.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS svd(
        Item_Code TEXT,
        Name TEXT,
        Brand TEXT,
        Price TEXT,
        Price_Discont TEXT,
        Link TEXT);
    """)
    conn.commit()
    conn.executemany("INSERT INTO svd(Item_Code, Name, Brand, Price, Price_Discont, Link) VALUES(?, ?, ?, ?, ?, ?);", data)
    conn.commit()
    conn.close()

def main():
    data = []
    count_page=1
    url = "https://www.sivasdescalzo.com/uk/footwear?p="+str(count_page)
    soup, next_page = createDriver(url, count_page)
    while True:
        pars(soup, data)
        if next_page:
            count_page+=1
            url = "https://www.sivasdescalzo.com/uk/footwear?p="+str(count_page)
            soup, next_page = createDriver(url, count_page)
        else:
            break
    createDB(data=data)
    
if __name__ == '__main__':
    main()