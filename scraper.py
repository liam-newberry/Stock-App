# File created by: Liam Newberry
from bs4 import BeautifulSoup
from excel import *
# import requests 
from urllib import request

# website = "https://finance.yahoo.com/quote/AAPL?p=AAPL"
# page = request.urlopen(website)

# soup =  BeautifulSoup(page, features='lxml')
# html = soup.prettify()

# print(type(html))
# box = soup.find('table', class_ ="W(100%) M(0)")

# f = box.find("h1").get_text()
# print(f)
create_graph('a')
