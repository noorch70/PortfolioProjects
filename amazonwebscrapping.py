#Step1 : Importing libraries
from bs4 import BeautifulSoup
import requests
import datetime
import time
import smtplib
import csv
from decimal import Decimal
 #Step2 : Connecting to website and pulling out title and price of item (since the project is automated, the csv file for price tracking is created the first time and then appended through the function)
# url='https://www.amazon.com/Conair-Double-Ceramic-Curling-1-inch/dp/B07CKKGR83/ref=sr_1_5?dchild=1&keywords=curling+iron&qid=1632600137&sr=8-5'
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36","Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
# page=requests.get(url,headers=headers)
# soup1=BeautifulSoup(page.content,"html.parser")
# soup2=BeautifulSoup(soup1.prettify(),"html.parser")
# title=soup2.find(id='productTitle').get_text()
# #pulling title
# title=title.strip()
# print(title)
# #pulling price
# price=soup2.find(id='price_inside_buybox').get_text()
# price=price.strip()


# print(price)
#generating date log
# today=datetime.date.today()
# header=['Title','Price','Date']
# data=[title,price,today]
#Step3: Creating a csv file
# with open('amazondata1.csv','w+',newline='',encoding='UTF8') as f:
#  writer=csv.writer(f)
#  writer.writerow(header)
#  writer.writerow(data)

 
#  #Step4: now appending the data to csv

# with open('amazondata.csv','a+',newline='',encoding='UTF8') as f:
#  writer=csv.writer(f)
#  writer.writerow(data)
#  #now putting this together in a function
#the above code is now just put in function 'check_price'
def check_price():
 #connect to website
 url='https://www.amazon.com/Conair-Double-Ceramic-Curling-1-inch/dp/B07CKKGR83/ref=sr_1_5?dchild=1&keywords=curling+iron&qid=1632600137&sr=8-5'
 headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36","Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
 page=requests.get(url,headers=headers)
 soup1=BeautifulSoup(page.content,"html.parser")
 soup2=BeautifulSoup(soup1.prettify(),"html.parser")
 title=soup2.find(id='productTitle').get_text()
#pulling title
 title=title.strip()
#pulling price
 price=soup2.find(id='price_inside_buybox').get_text()
 price=price.strip()
 #generating datelog
 today=datetime.date.today()
 header=['Title','Price','Date']
 data=[title,price,today]
 #appending the data to csv file
 with open('amazondata.csv','a+',newline='',encoding='UTF8') as f:
  writer=csv.writer(f)
  writer.writerow(data)
 price_int=Decimal(price.strip('$'))
 return price_int


#Step5 : send_mail function will inform me via email if the price of the item goes below $15
def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login('noorfatimach70@gmail.com','Mamapapa1:@')
    
    subject = "The curler you want is below $15! Now is your chance to buy!"
    body = "This is the moment we have been waiting for. Now is your chance. Don't mess it up!The curler is now below $15"
   
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(subject,'noorfatimach70@gmail.com',body)

price_int=check_price()

if(price_int<15):
 send_mail()
