import requests
from google_email import send_email
from bs4 import BeautifulSoup
from models import *
from csv_creater import add_header, append_row


def scraping_single_page(link, num):
   url = 'https://books.toscrape.com/catalogue/' + link
   response = requests.get(url)
   soup = BeautifulSoup(response.content, "html.parser")
   result = soup.find('div', class_="content")
   pro_title = "" if result.find('h1') == None else result.find('h1').text
   pro_price = "" if result.find('p', class_='price_color') == None else result.find('p', class_='price_color').text
   pro_desc = "" if result.find('p', {'class': False, 'id': False}) == None  else result.find('p', {'class': False, 'id': False}).text
   pro_details = {'Title' : pro_title, 'Price' : pro_price, 'Description' : pro_desc, 'Page' : num}
   book = Book(title=pro_title, price=pro_price, description=pro_desc, page = num)
   session.add(book)
   try:
    session.commit()
    append_row(pro_details)
   except exc.SQLAlchemyError:
    session.rollback()

def scraping_main_page(num):
   num = str(num)
   url = f'https://books.toscrape.com/catalogue/page-{num}.html'
   response = requests.get(url)
   soup = BeautifulSoup(response.content, "html.parser")
   product_links = soup.find_all('a', attrs={"title":True})
   for link in product_links:
    scraping_single_page(link.get("href"), num)

def pagination():
  url = 'https://books.toscrape.com/'
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  pages_str = soup.find('li', class_='current')
  maxpages = int(pages_str.string.strip()[-2:])
  add_header()

  last_book = session.query(Book).order_by(Book.id.desc()).first()

  if last_book == None:
    for i in range(1,maxpages+1):
      scraping_main_page(i)
  elif last_book.page == maxpages:
    pass
  else:
    for i in range(last_book.page,maxpages+1):
      scraping_main_page(i)
  send_email()

pagination()
