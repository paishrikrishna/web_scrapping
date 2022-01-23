import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
data = {}



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
    return add_data


def extract_data(url):
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")

    result_container = soup.find_all("div", {"class": "results-section regular-searchpage"})

    for individual in result_container:
        image_res = []
        name_res = []
        lat_res = []
        long_res = []
        link_res = []
        add_data = []
        res = individual.find_all("div", {"class": "results-card-ecommerce"})
        for img in res:
            image = img.find_all("div",{"class":"cover lazy"})
            for i in image:
                #print(i.get("data-src"))
                image_res.append(i.get("data-src"))
        for n in res:
            name = n.find_all("span",{"class","vendorname-span"})
            for nm in name:
                #print(nm.text)
                name_res.append(nm.text)
        for l in res:
            lat = l.find_all("div",{"class","geofitdata mui--hide"})
            for lt in lat:
                #print(lt.get("data-lat"),lt.get("data-lon"))
                lat_res.append(lt.get("data-lat"))
                long_res.append(lt.get("data-lon"))

        for a in res:
            href = a.find_all("a",{"class":"vendor-card"})
            for link in href:
                link_res.append("https://www.fitternity.com"+link.get("href"))
                add_data.append(extract_add_data(link_res[-1]))



    for i in range(len(image_res)):
        test = {}
        test["image"] = image_res[i]
        test["lat"] = lat_res[i]
        test["lon"] = long_res[i]
        test["href"] = link_res[i]
        test["additional_details"] = add_data[i]
        data[name_res[i]] = test

    return data

print(extract_data("https://www.fitternity.com/mumbai/fitness"))
