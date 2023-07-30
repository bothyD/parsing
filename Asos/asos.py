import requests
import json
import sqlite3
 
def crete_request(url):
    response = requests.get(url=url)
    print(response.status_code)    
    return response.text

def pars(krosi1, data):
    for kros in krosi1:
        links ="https://www.asos.com/truffle-collection/" + kros['url']
        name = kros['name']
        brand = kros['brandName']
        item_code = kros['id']

        price = kros['price']['previous']['text']
        price2 = kros['price']['rrp']['text']
        if (price + price2) == "":
            price = kros['price']['current']['value']
            price_discont = ''
        else:
            price_discont = kros['price']['current']['value']
            if price == "":    
                price = kros['price']['rrp']['value']
            else:
                price = kros['price']['previous']['value']
        
        stroka = (item_code, name, brand, price, price_discont, links)
        data.append(stroka)

def createDB(data):
    
    conn = sqlite3.connect('/home/pavlo/pavlik/python/bot_for_IOri/chromedriver/pars_foots.db')
    
    conn.execute("""CREATE TABLE IF NOT EXISTS asos(
        Item_Code TEXT,
        Name TEXT,
        Brand TEXT,
        Price TEXT,
        Price_Discont TEXT,
        Link TEXT);
    """)
    conn.commit()
    conn.executemany("INSERT INTO asos(Item_Code, Name, Brand, Price, Price_Discont, Link) VALUES(?, ?, ?, ?, ?, ?);", data)
    conn.commit()
    conn.close()

def main():
    data = []
    countPage = 0
    url = 'https://www.asos.com/api/product/search/v2/categories/4209?offset='+str(countPage) +'&store=COM&lang=en-GB&currency=GBP&rowlength=4&channel=desktop-web&country=GB&keyStoreDataversion=ornjx7v-36&limit=200'
    soup = crete_request(url=url)
    krosi = json.loads(soup)
    krosi1 = krosi['products']    
    pars(krosi1, data)
    itemCount = int(krosi['itemCount'])
    while itemCount > countPage:
        countPage+=200
        url = 'https://www.asos.com/api/product/search/v2/categories/4209?offset='+str(countPage) +'&store=COM&lang=en-GB&currency=GBP&rowlength=4&channel=desktop-web&country=GB&keyStoreDataversion=ornjx7v-36&limit=200'
        soup = crete_request(url=url)
        krosi = json.loads(soup)
        krosi1 = krosi['products']    
        pars(krosi1, data)
    createDB(data=data)    

if __name__ == '__main__':
    main()
