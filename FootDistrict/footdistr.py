import undetected_chromedriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import sqlite3
driver = undetected_chromedriver.Chrome()
data = []

def createDriver(url):
    print("creat driver")
    try: 
        driver.get(url=url)
        time.sleep(45)
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(1)
        actions1 = ActionChains(driver)
        actions1.send_keys(Keys.SPACE).perform()
        time.sleep(25)
        driver.get(url)
        time.sleep(10)
        main_page = driver.page_source
        soup = BeautifulSoup(main_page, 'lxml')
        if(proverka_kapchi(soup)):
            createDriver(url)
        else:  
            swap_page() 
    except Exception as ex:
        print(ex)
        
def swap_page():
    print("start - swap page") 
    while(True):
        main_page = driver.page_source
        soup = BeautifulSoup(main_page, 'lxml')
        #proverka kapchi
        if(proverka_kapchi(soup)):
            print("\nВ поиске появилась капча\n")
            current_url = add_one_to_page(current_url)
            createDriver(current_url)
            return
        ################
        pars(soup=soup)     
        current_url = driver.current_url
        current_page(current_url)
        try:
            button = driver.find_element("css selector", "li.item.pages-item-next a.action.next")
            driver.execute_script("arguments[0].click();", button)
        except Exception:
            print("not found")
            return 
        time.sleep(10)

def pars(soup):   
    krosi = soup.find_all('li', class_='item product product-item basic')
    for kros in krosi:
        krossovok = kros.find('a', class_="product photo product-item-photo")
        item_code = krossovok.get('data-id')
        brand = krossovok.get('data-brand')
        name = krossovok.get('data-name')
        links = krossovok.get('href')
        try:
            price_get = kros.find(class_="price-box price-final_price")
            price_discont = price_get.find(class_='special-price').find(class_="price").text
            price = price_get.find(class_='old-price').find(class_="price").text
        except Exception:
            price_discont = krossovok.get('data-price')
            price = "-"
        stroka = (item_code, name, brand, price, price_discont, links)
        data.append(stroka)                 

def add_one_to_page(current_url):
    index_count = current_url.index('=')
    plus_page = int(current_url[index_count+1: len(current_url)])+1
    current_url  = current_url[0:index_count+1] + str(plus_page)
    return current_url

def proverka_kapchi(soup):
    try:
        proverka = soup.find('h2', {"id": "challenge-running"}).text
        if proverka == "Проверка безопасности подключения к сайту":    
            print("kaptcha - true")
            return True
    except Exception:
        
        return False

def current_page(url):
    index_count = url.index('=')  
    current_page  = url[index_count+1 : len(url)]
    print(f"Текущая страница - {current_page}")

def createDB():
    conn = sqlite3.connect('/home/pavlo/pavlik/python/bot_for_IOri/chromedriver/pars_foots.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS footdistrict(
        Item_Code TEXT,
        Name TEXT,
        Brand TEXT,
        Price TEXT,
        Price_Discont TEXT,
        Link TEXT);
    """)
    conn.commit()
    conn.executemany("INSERT INTO footdistrict(Item_Code, Name, Brand, Price, Price_Discont, Link) VALUES(?, ?, ?, ?, ?, ?);", data)
    conn.commit()
    conn.close()

def main():
    url = "https://footdistrict.com/calzado/?p=1"
    createDriver(url=url)
    driver.close()
    driver.quit()
    #createDB()
   
if __name__ == '__main__':
    main()   
