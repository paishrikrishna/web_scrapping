import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import xlwt
from xlwt import Workbook

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Gym Details')
sheet2 = wb.add_sheet('Membership Plans')
sheet2_counter = 0
sheet1_counter = 0

sheet1.write(0,0,'Name')
sheet1.write(0,1,'Latitude')
sheet1.write(0,2,'Longitude')
sheet1.write(0,3,'Fitternity Page Link')
sheet1.write(0,4,'Address')
sheet1.write(0,5,'City')
sheet1.write(0,6,'Activities')
sheet1.write(0,7,'Total Reivew')
sheet1.write(0,8,'Overall Rating')
sheet1.write(0,9,'Facility Ratings')
sheet1.write(0,10,'Instructor Ratings')
sheet1.write(0,11,'Vibe Ratings')
sheet1.write(0,12,'Value For Money Ratings')
sheet1.write(0,13,'Equipment Ratings')
sheet1.write(0,14,'Aminities')
sheet1.write(0,15,'Extra Info')


sheet2.write(0,0,'Gym Name')
sheet2.write(0,1,'Plan Name')
sheet2.write(0,2,'Price in Rs.')

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


        ratings["total_ratings_and_reviews"] = soup.find("div",{"class":"mui-col-md-10 mui-col-xs-12"}).find("div",{"class":"heading-text section-header"}).find("span").text.split("(")[1].split(")")[0]
    except:
        pass

    try:
        ratings["average_ratings_overall"] = soup.find("div",{"class":"rating-review-block"}).find("div",{"class":"mui-col-xs-12 mui-col-md-12 average-rating"}).find("span").text
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

    global sheet1_counter

    for i in range(len(image_res)):
        test = {}
        test["name"] = name_res[i]
        test["image"] = image_res[i]
        test["lat"] = lat_res[i]
        test["lon"] = long_res[i]
        test["href"] = link_res[i]
        test["additional_details"] = add_data[i]
        data[str(i)] = test
        try:
            sheet1.write(sheet1_counter+i+1,0,name_res[i])
        except:
            sheet1.write(sheet1_counter+i+1,0,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,1,lat_res[i])
        except:
            sheet1.write(sheet1_counter+i+1,1,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,2,long_res[i])
        except:
            sheet1.write(sheet1_counter+i+1,2,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,3,link_res[i])
        except:
            sheet1.write(sheet1_counter+i+1,3,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,4,add_data[i]["address"])
        except:
            sheet1.write(sheet1_counter+i+1,4,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,5,add_data[i]["city"])
        except:
            sheet1.write(sheet1_counter+i+1,5,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,6," ".join(add_data[i]["activities"]))
        except:
            sheet1.write(sheet1_counter+i+1,6,"NULL")

        #print(add_data[i]["ratings"])

        try:
            sheet1.write(sheet1_counter+i+1,7,add_data[i]["ratings"]["total_ratings_and_reviews"])
        except:
            sheet1.write(sheet1_counter+i+1,7,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,8,add_data[i]["ratings"]["average_ratings_overall"])
        except:
            sheet1.write(sheet1_counter+i+1,8,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,9,add_data[i]["ratings"]["average_facilities"])
        except:
            sheet1.write(sheet1_counter+i+1,9,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,10,add_data[i]["ratings"]["average_instructor"])
        except:
            sheet1.write(sheet1_counter+i+1,10,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,11,add_data[i]["ratings"]["average_vibe"])
        except:
            sheet1.write(sheet1_counter+i+1,11,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,12,add_data[i]["ratings"]["average_value_for_money"])
        except:
            sheet1.write(sheet1_counter+i+1,12,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,13,add_data[i]["ratings"]["average_equipment"])
        except:
            sheet1.write(sheet1_counter+i+1,13,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,14," ".join(add_data[i]["aminities"]))
        except:
            sheet1.write(sheet1_counter+i+1,14,"NULL")

        try:
            sheet1.write(sheet1_counter+i+1,15," ".join(add_data[i]["extra_info"]))
        except:
            sheet1.write(sheet1_counter+i+1,15,"NULL")

        global sheet2_counter
        plans_details = list(add_data[i]["plan"].keys())
        plans_values = list(add_data[i]["plan"].values())

        for j in range(sheet2_counter,sheet2_counter+len(plans_details)):
            try:
                sheet2.write(j+1,0,name_res[i])
            except:
                sheet2.write(j+1,0,"NULL")
            try:
                sheet2.write(j+1,1,plans_details[j-sheet2_counter])
            except:
                sheet2.write(j+1,1,"NULL")
            try:
                sheet2.write(j+1,2,str(plans_values[j-sheet2_counter]).replace("{","").replace("}",""))
            except:
                sheet2.write(j+1,2,"NULL")

        sheet2_counter += len(plans_details)
        #print(plans_details)
        #print(plans_values)
    sheet1_counter += len(image_res)
    return data



if __name__ == '__main__':
    data_final = []
    for i in range(1,10):
        data_final.append(extract_data("https://www.fitternity.com/mumbai/fitness?page="+str(i)))
        if i/10 == 0:
            time.sleep(10)

    wb.save('fitternity_scrapped_data.xls')
    print(data_final)
