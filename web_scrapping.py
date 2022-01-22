import requests
from bs4 import BeautifulSoup
data = {}
req = requests.get("https://www.fitternity.com/mumbai/fitness")

soup = BeautifulSoup(req.content, "html.parser")

result_container = soup.find_all("div", {"class": "results-section regular-searchpage"})

for individual in result_container:
    image_res = []
    name_res = []
    lat_res = []
    long_res = []
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



for i in range(len(image_res)):
    test = {}
    test["image"] = image_res[i]
    test["lat"] = lat_res[i]
    test["lon"] = long_res[i]
    data[name_res[i]] = test
print(len(data))

#print(res)
