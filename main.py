import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()



## Item Url Inside
url= requests.get(os.getenv("ITEM_URL"))   

## YOUR UNSAFE EMAIL "example@example.com"
email = os.getenv("EMAIL")  

##PASSWORD OF UNSAFE EMAIL "randompassword"
email_password = os.getenv("EMAIL_PASSWORD") 

## YOUR EMAIL "myemail@email.com"
to_email = os.getenv("TO_EMAIL") 

raw_html = url.text

soup = BeautifulSoup(raw_html, "html.parser")

price_div = soup.find("div", class_="product-price-container")

try:
    child = price_div.findChild('span', class_="prc-dsc")
    price = float(child.text.replace(",", ".").split(" ")[0])
except:
    child = price_div.findChild('span', class_="prc-slg")
    price = float(child.text.replace(",", ".").split(" ")[0])


item_name = soup.find("h1", class_="pr-new-br").text
print(price, item_name)

msg = f"Subject:Price Alert on {item_name} \n\n Price is {price}".encode("UTF-8")

if price < 500:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email, password=email_password)
        connection.sendmail(
            from_addr=email,
            to_addrs=to_email,
            msg=msg
        )
