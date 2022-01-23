from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


#driver = webdriver.Chrome(executable_path='/home/shri/Desktop/GitHub/web_scrapping/chromedriver')
#driver.maximize_window()
#driver.get(url)



def extract_add_data(url):

    add_data = {}
    #req = requests.get(url)

    #soup = BeautifulSoup(req.content,"html.parser")

    browser = webdriver.Chrome(executable_path="/home/shri/Desktop/GitHub/web_scrapping/chromedriver")
    browser.get(url)
    soup = BeautifulSoup(browser.page_source,"html.parser")

    adr = soup.find_all("div",{"class":"location-text"})

    for address in adr:
        add_data["address"] = address.text

    loc = soup.find_all("div",{"class":"location-value"})

    for city in loc:
        add_data["city"] = city.text

    rate_cards = soup.find_all("div",{"class":"mui-row rate-item ratecard-vertical-center"})

    plans = {}
    for i in range(len(rate_cards)):
         duration = rate_cards[i].find("div",{"class":"mui-col-md-8 mui-col-xs-12 ratecard-duration"})
         prices = rate_cards[i].find("span",{"id":"offer"})
         if prices == None:
             prices = rate_cards[i].find_all("span")[1]
         period = duration.text.split(" ")

         plans[period[0]+" "+period[1]] = prices.text

    add_data["plans"] = plans
    print(add_data)

#extract_add_data("https://www.fitternity.com/xff---xtreme-fight-federation-lokhandwala-lokhandwala")
for i in range(2):
    browser = webdriver.Chrome(executable_path="/home/shri/Desktop/GitHub/web_scrapping/chromedriver")
    browser.get("https://www.fitternity.com/xff---xtreme-fight-federation-lokhandwala-lokhandwala")
    soup = BeautifulSoup(browser.page_source,"html.parser")
