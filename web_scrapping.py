import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

data = {}



def extract_add_data(url):

    add_data = {}
    #req = requests.get(url)

    #soup = BeautifulSoup(req.content,"html.parser")

    browser = webdriver.Chrome(executable_path="/home/shri/Desktop/GitHub/web_scrapping/chromedriver")
    browser.get(url)
    browser.maximize_window()

    soup = BeautifulSoup(browser.page_source,"html.parser")

    adr = soup.find_all("div",{"class":"location-text"})

    for address in adr:
        add_data["address"] = address.text

    loc = soup.find_all("div",{"class":"location-value"})

    for city in loc:
        add_data["city"] = city.text

    activities = []

    try:
        acts = soup.find("div",{"class":"serviceofferinglinks"}).find("ul")
        acts_name = acts.find_all("li",{"class":"serviceoffer"})
        for act in acts_name:
            activities.append(act.text)

    except:
        pass
    add_data["activities"] = activities

    actions = ActionChains(browser)
    categories = []
    plan = {}


    try:
        rate_card_section = browser.find_element_by_xpath("//div[@class='container-info mui-row ratecard-container']")
        individual_rates_section = rate_card_section.find_elements_by_xpath("//div[@class='icon-block']")

        actions.move_to_element(individual_rates_section[0]).perform()
        individual_rates_section[0].click()

        category = soup.find_all("div",{"class":"service-name mui-col-md-9"})
        for i in category:
            if i.get("data-service-name") not in categories:
                categories.append(i.get("data-service-name"))

        for i in individual_rates_section:
            actions.move_to_element(i).perform()
            #time.sleep(5)
            i.click()

    except:
        pass


    try:

        card = soup.find_all("div",{"class","mui-col-xs-12 service-detail-container"})

        for i in range(len(card)):
            plans = {}
            indi_plan = card[i].find_all("div",{"class":"mui-row ratecard-vertical-center"})
            for r in indi_plan:
                duration = r.find("span",{"class":"duration"})
                duration_extra = r.find("span",{"id":"offer","class":"duration"})
                if duration_extra == None:
                    duration_extra_text = ""
                else:
                    duration_extra_text = " " + duration_extra.text
                prices = r.find("span",{"id":"offer","itemprop":"price"})
                if prices == None:
                    prices = r.find("div",{"class":"mui-col-md-4 mui-col-xs-12 ratecard-price"})
                if duration == None:
                    duration = r.find("div",{"class":"mui-col-md-8 mui-col-xs-12 ratecard-duration"})
                plans[duration.text + duration_extra_text] = prices.text
            plan[categories[i]] = plans
    except:
        pass
    add_data["plan"] = plan

    ratings = {}
    try:
        aminities_section = browser.find_element_by_xpath("//div[@class='mui-container']")
        actions.move_to_element(aminities_section).perform()


        ratings["total_ratings_and_reviews"] = soup.find("div",{"class":"heading-text section-header"}).find("span").text.split("(")[1].split(")")[0]
    except:
        pass

    try:
        ratings["average_ratings_overall"] = soup.find("div",{"class":"rating-review-block"}).find("span",{"class":"overall-rating avg-rating color8"}).text
        average_ratings = soup.find("div",{"class":"rating-review-block"}).find_all("span",{"class":"counting-span"})
        ratings["average_facilities"] = average_ratings[0].text
        ratings["average_instructor"] = average_ratings[1].text
        ratings["average_vibe"] = average_ratings[2].text
        ratings["average_value_for_money"] = average_ratings[3].text
        ratings["average_equipment"] = average_ratings[4].text


    except:
        pass

    add_data["ratings"] = ratings

    aminities = []
    try:
        aminities_section = browser.find_element_by_xpath("//div[@class='container-info mui-row']")
        actions.move_to_element(aminities_section).perform()


        aminities_section = soup.find("div",{"class":"container-info mui-row"})
        aminities_name = aminities_section.find_all("div",{"class":"title"})
        for i in aminities_name:
            if "inactive-facility" not in i.get("class"):
                aminities.append(i.find("span").text)


    except:
        pass

    add_data["aminities"] = aminities

    extras = []
    try:
        extra_info = aminities_section.find("div",{"class":"mui-col-md-12 subofferings hidemobile"})
        extra_items = extra_info.find_all("div",{"class":"tag"})
        for i in extra_items:
            if i.find("span").text not in extras:
                extras.append(i.find("span").text)

    except:
        pass

    add_data["extra_info"] = extras

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
        test["name"] = name_res[i]
        test["image"] = image_res[i]
        test["lat"] = lat_res[i]
        test["lon"] = long_res[i]
        test["href"] = link_res[i]
        test["additional_details"] = add_data[i]
        data[str(i)] = test

    return data

print(extract_data("https://www.fitternity.com/mumbai/fitness"))
