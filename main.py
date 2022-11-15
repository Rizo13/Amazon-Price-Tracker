import requests
from bs4 import BeautifulSoup
import smtplib
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

URL = "https://www.amazon.com/International-Version-Introducing-Paperwhite-auto-adjusting/dp/B08N2ZL7PS/ref" \
      "=nav_custrec_signin?crid=38RRM8TTDPK3N&keywords=kindle+paperwhite+2022&qid=1668501812&sprefix=kindle%2Caps" \
      "%2C210&sr=8-6 "

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/107.0.0.0 Safari/537.36',
    'Accept-Language': "hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7,bs;q=0.6,sl;q=0.5,sr;q=0.4,de;q=0.3,es;q=0.2",
}

response = requests.get(URL, headers=headers)
lxml_doc = response.text

soup = BeautifulSoup(lxml_doc, 'lxml')
product_name = soup.title.string[12:80]
print(product_name)

try:
    product_price = int(soup.find(name="span", class_="a-price-whole").getText()[:3])
    print(product_price)
    if product_price < 150:
        Subject = "Amazon low price alert"
        Text = f"Hello, your {product_name} now costs {product_price}$. Check it out via {URL}"
        message = f'Subject: Amazon low price alert\n\nHello, your {product_name} now costs {product_price}$. Check it out via {URL}'
        with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
            smtp.starttls()
            smtp.login(user=EMAIL, password=PASSWORD)
            smtp.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=message.encode('utf-8'))
except AttributeError:
    print("Can't Fetch data.")


