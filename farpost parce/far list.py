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


def get_html(url):
	r = requests.get(url)
	return r.text


def write_csv(arr): 
	f = open('farpost list.txt', 'w')
	for a in arr:
		f.write(a + '\n')
	f.close()

def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	divs = soup.find('div', class_='options itemsAll')
	td = divs.find('td', class_='col1')
	vacs = td.find_all('div', class_='item')
	arr = [] 
	for vac in vacs:
		try:
			url = vac.find('a', class_='option').get('href')
		except:
			url = ''
		arr.append(url)
	td = divs.find('td', class_='col2')
	vacs = td.find_all('div', class_='item')
	for vac in vacs:
		try:
			url = vac.find('a', class_='option').get('href')
		except:
			url = ''
		arr.append(url)
	write_csv(arr)	


def main():
	print('Начало работы программы')
	url = "https://www.farpost.ru/vladivostok/job/vacancy/"
	html = get_html(url)
	get_page_data(html)


if __name__ == '__main__':
	main()


