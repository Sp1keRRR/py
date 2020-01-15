from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import csv
from random import choice
import time
import random
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os.path
import datetime



def get_html(url):
	r = requests.get(url)
	return r.text


def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pagesall = soup.find('div', class_='pagebar')
	if pagesall is None:
		return 1 
	else:
		pagelast = pagesall.find_all('a', class_='page')[-1].get('href')
		total_pages = pagelast.split('=')[1]    
		return int(total_pages)

def write_log(db):
	daytime = datetime.datetime.today().strftime("%m/%d/%Y")
	with open('farpost log.txt', 'a') as file:
		writer = csv.writer(file)
		writer.writerow((db['daytime'],
						db['log']))	 

def write_csv(db): 
	count = 0
	try:
		with open('farpost.txt') as file:
			for line in file:
				if db['url_user'] in line:
					count += 1
					break
		if count > 0:
			print("Юзер "+ db['url_user'] + " уже присутствует")
			#Лог
			daytime = datetime.datetime.today().strftime("%Y/%m/%d-%H.%M.%S")
			log = "Юзер "+ db['url_user'] + " уже присутствует"
			db = {'daytime':daytime,
				'log':log}
			write_log(db)
		else:
			with open('farpost.txt', 'a') as file:
				writer = csv.writer(file)
				writer.writerow((db['title'],
								db['price'],
								db['city'],
								db['data'],
								db['phone'],
								db['email'],
								db['professionalArea'],
								db['url_user'],
								db['url']))
	except:
		with open('farpost.txt', 'a') as file:
			writer = csv.writer(file)
			writer.writerow((db['title'],
							db['price'],
							db['city'],
							db['data'],
							db['phone'],
							db['email'],
							db['professionalArea'],
							db['url_user'],
							db['url']))


def get_page_data(html, driver, captcha):

	soup = BeautifulSoup(html, 'lxml')
	divs = soup.find('tbody', class_='native')
	ads = divs.find_all('tr', class_='bull-item -exact')
	i = 0 
	for ad in ads:
		i += 1
		try:
			title = ad.find('td', class_='descriptionCell').find('a', class_='bulletinLink auto-shy').contents[0]
		except:
			title = ''

		try:
			ref = ad.find('td', class_='descriptionCell').find('a', class_='bulletinLink auto-shy').get('href')
			url = "https://www.farpost.ru" + ref
		except:
			url = ''
		#Открывалась ли страница ранее
		if os.path.exists('farpost.txt'):
			count = 0
			with open('farpost.txt') as file:
				for line in file:
					if url in line:
						count += 1
						break
			if count > 0:
				#print("Странница "+ url + " открывалась ранее")
				print('Процесс на странице %d%%' % (i/len(ads)*100))
				#Лог
				daytime = datetime.datetime.today().strftime("%Y/%m/%d-%H.%M.%S")
				log = ('Процесс на странице %d%%' % (i/len(ads)*100))
				db = {'daytime':daytime,
					'log':log}
				write_log(db)
				#time.sleep(30)
				continue
		else:
			open('farpost.txt', 'a')

		driver.get(url)
		#Капча при переходе на другую страницу
		if driver.current_url != url:
			print('Капча...Перезагрузка браузера')
			#Лог
			daytime = datetime.datetime.today().strftime("%Y/%m/%d-%H.%M.%S")
			log = 'Капча...Перезагрузка браузера'
			db = {'daytime':daytime,
				'log':log}
			write_log(db)

			driver.quit()
			rNum = 120
			time.sleep(rNum)
			driver.get(url)
			# print('Введите капчу для продолжения работы (10 мин)')
			# try:
			# 	element = WebDriverWait(driver, 600).until(
			# 		EC.presence_of_element_located((By.XPATH,'//a[@class="button bigbutton viewbull-summary__button viewbull-summary__button_job"]'))
			# 	)
			# except:
			# 	captcha = 2
			# 	driver.quit()
			# 	break 
			# finally:
			# 	if captcha == 2:
			# 		print('Капча не пройдена')
			# 		break
			# 	print('Капча пройдена')
			# 	driver.get(url)
				
		rNum = 60
		time.sleep(rNum)

		try:
			url_user_text = driver.find_element_by_class_name('userNick').text
			url_user = driver.find_element_by_link_text(url_user_text).get_attribute('href')
		except:
			try:
				url_user_text = driver.find_element_by_class_name('company-name').text
				url_user = driver.find_element_by_link_text(url_user_text).get_attribute('href')
			except:
				url_user = ""
		
		#Поиск на присутствие пользователя в файле
		if os.path.exists('farpost.txt'):
			count = 0
			with open('farpost.txt') as file:
				for line in file:
					if url_user in line:
						count += 1
						break
			if count > 0:
				#print("Юзер "+ url_user + " уже присутствует")
				time.sleep(60)
				print('Процесс на странице %d%%' % (i/len(ads)*100))
				#Лог
				daytime = datetime.datetime.today().strftime("%Y/%m/%d-%H.%M.%S")
				log = ('Процесс на странице %d%%' % (i/len(ads)*100))
				db = {'daytime':daytime,
					'log':log}
				write_log(db)
				continue
		else:
			open('farpost.txt', 'a')

		#Капча-картинка после нажатия кнопки
		try:
			element = driver.find_element_by_xpath('//a[@class="button viewAjaxContacts viewbull-summary__button bottom-button-wrap bulletin-contacts-button"]')
			element.click()
			try:
				captchaPic = driver.find_element_by_class_name('bzr-captcha__image')
				print('Введите капчу для продолжения работы (20 секунд)')
				#Лог
				daytime = datetime.datetime.today().strftime("%Y/%m/%d-%H.%M.%S")
				log = 'Введите капчу для продолжения работы (20 секунд)'
				db = {'daytime':daytime,
					'log':log}
				write_log(db)

				time.sleep(20)
			except:
				time.sleep(1)
			rNum = 120 
			time.sleep(rNum)
			email = driver.find_element_by_class_name('emailLink').text 
		except:
			email = ''
		try:
			phone = driver.find_element_by_xpath('//*[@class="new-contacts__td new-contact__phone"]').text
			phone = phone.strip()
		except:
			phone = ""
		try:
			priceFull = driver.find_element_by_xpath('//*[@data-field="salaryMin-salaryMax-salaryDescription"]').text
			price = priceFull.strip()
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
		try:
			professionalArea = driver.find_element_by_xpath('//*[@data-field="professionalArea"]').text
			professionalArea = professionalArea.strip()
		except:
			professionalArea = ""

		db = {'title':title,
				'price':price,
				'city':city,
				'data':data,
				'phone':phone,
				'email':email,
				'professionalArea':professionalArea,
				'url_user':url_user,
				'url':url}
		write_csv(db)
		
		print('Процесс на странице %d%%' % (i/len(ads)*100))
		#Лог
		daytime = datetime.datetime.today().strftime("%Y/%m/%d-%H.%M.%S")
		log = ('Процесс на странице %d%%' % (i/len(ads)*100))
		db = {'daytime':daytime,
			'log':log}
		write_log(db)

		#Через сколько перезагрузка браузера
		if i % 1000000 == 0:
			driver.quit()
			rNum = random.randint(10,20)
			print('Отдых %d секунд на %d%%' % (rNum, i/len(ads)*100))
			time.sleep(rNum)
			driver = webdriver.Firefox()

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
	#proxies = {'https': 'ipaddress:5000'}
	p = get_proxy() # {'schema': '', 'address': ''}

	proxy = { p['schema']: p['address']  }
	#r = requests.get(url, proxies=proxy, timeout=5
	#return r.json()['origin']
	return p['address']

def main():
	#Лог
	log = 'Начало работы программы'
	daytime = datetime.datetime.today().strftime("%Y/%m/%d-%H.%M.%S")
	print(log)
	print(daytime)
	db = {'daytime':daytime,
			'log':log}
	write_log(db)
	
	url_arr = []
	with open('farpost list.txt') as file:
			for line in file:
				url_arr.append(line)
	
	#url = "https://www.farpost.ru/vladivostok/job/vacancy/+/%D1%E8%F1%F2%E5%EC%ED%FB%E9+%E0%E4%EC%E8%ED%E8%F1%F2%F0%E0%F2%EE%F0/"
	
	driver = webdriver.Firefox()
	for url_page in url_arr:
		print('Странница: ' + url_page)
		#Лог
		log = 'Странница: ' + url_page
		daytime = datetime.datetime.today().strftime("%Y/%m/%d-%H.%M.%S")
		db = {'daytime':daytime,
			'log':log}
		write_log(db)

		base_url = url_page + "?page="
	
	
		total_pages = get_total_pages(get_html(url_page))

	
		captcha = 1
		if total_pages == 1:
			url_gen = url_page 
			html = get_html(url_gen)
			get_page_data(html, driver, captcha)
		else:
			for i in range(1, total_pages):
				url_gen = base_url + str(i) 
				html = get_html(url_gen)
				get_page_data(html, driver, captcha)
				if captcha == 2:
					break
	driver.quit()

if __name__ == '__main__':
	main()


