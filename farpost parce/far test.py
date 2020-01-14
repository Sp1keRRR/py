from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import csv
from random import choice
import time
from selenium.webdriver.firefox.options import Options



def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pagesall = soup.find('div', class_='pagebar')
    pagelast = pagesall.find_all('a', class_='page')[-1].get('href')
    total_pages = pagelast.split('=')[1]
    return int(total_pages)

def write_csv(db):
    with open('farpost.txt', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((db['title'],
                         db['price'],
                         db['city'],
                         db['data'],
                         db['email'],
                         db['url']))



def get_page_data(html):

    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('tbody', class_='native')
    ads = divs.find_all('tr', class_='bull-item -exact')
    for ad in ads:
        try:
            title = ad.find('td', class_='descriptionCell').find('a', class_='bulletinLink auto-shy').contents[0]
        except:
            title = ''
        try:
            ref = ad.find('td', class_='descriptionCell').find('a', class_='bulletinLink auto-shy').get('href')
            url = "https://www.farpost.ru" + ref
        except:
            url = ''

        try:
            priceFull = ad.find('td', class_='descriptionCell').find('span', attrs={"data-role":"price"}).contents[0].split(' ')
            firstPrice = priceFull[0].replace("\xa0",'')
            price = firstPrice[0].replace("\xa0",'')
        except:
            price = ''
        try:
            data = ad.find('td', class_='dateCell').find('div', class_='date').contents[0]
        except:
            data = ''
        try:
            city = ad.find('td', class_='dateCell').find('div', class_='city').contents[0]
        except:
            city = ''

        db = {'title':title,
                'price':price,
                'city':city,
                'data':data,
                'email':email,
                'url':url}
        write_csv(db)

def get_proxy():
    html = requests.get('https://www.sslproxies.org').text
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:20]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        if schema == 'https':
            proxy = {'schema': schema, 'address': ip + ':' + port}
            proxies.append(proxy)

    return choice(proxies)

def get_html_proxy(url):
    # proxies = {'https': 'ipaddress:5000'}
    p = get_proxy() # {'schema': '', 'address': ''}

    proxy = { p['schema']: p['address']  }
    #r = requests.get(url, proxies=proxy, timeout=5
    #return r.json()['origin']
    return p['address']

def main():
    url = "https://www.farpost.ru/vladivostok/job/vacancy/kontroler-ohrannik-74295444.html"
    #base_url = url + "?page="


    #total_pages = get_total_pages(get_html(url))

    #urlMyIP = 'http://httpbin.org/ip'
    #proxyIP = get_html_proxy(urlMyIP)

    #caps = webdriver.DesiredCapabilities.FIREFOX
    #caps['marionette'] = True
    #caps['proxy'] = {
    #    "proxyType": "MANUAL",
    #    "httpProxy": proxyIP,
    #    "ftpProxy": proxyIP,
    #    "sslProxy": proxyIP
    #}

    #driver = webdriver.Firefox(capabilities=caps)
    driver = webdriver.Firefox()
    #print(proxyIP)
    # try:
    driver.get(url)
        #time.sleep(60)
        #element = driver.find_element_by_link_text('Информация о компании')
    element = driver.find_element_by_xpath('//a[@class="button viewAjaxContacts viewbull-summary__button bottom-button-wrap bulletin-contacts-button"]')
    element.click()
    emailLink = driver.find_element_by_class_name('emailLink')
    email = emailLink.text
    print(emailLink.text)
    # except:
    #     print("Nothing happened")

    # for i in range(1, total_pages):
    #     url_gen = base_url + str(i)
    #     html = get_html(url_gen)



        #get_page_data(html)


if __name__ == '__main__':
    main()
