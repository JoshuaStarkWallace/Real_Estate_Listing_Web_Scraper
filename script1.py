import requests
from bs4 import BeautifulSoup
import pandas

r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
df = pandas.DataFrame(1)

soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("div", {"class": "propertyRow"})

all[0].find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ", "")

l = []

base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0, 30, 10):
    print(base_url + str(page)+".html")
    r = requests.get(base_url + str(page)+".html")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class": "propertyRow"})

    # Pulling data from each listing and storing it in a dictionary.
    for item in all:
        d = {}
        try:
            d["Address"] = item.find_all("span", {"class", "propAddressCollapse"})[0].text
        except:
            d["Address"] = None

        try:
            d["Locality"] = item.find_all("span", {"class", "propAddressCollapse"})[1].text
        except:
            d["Locality"] = None

        try:
            d["Price"] = item.find("h4", {"class", "propPrice"}).text.replace("\n", "").replace(" ", "")
        except:
            d["Price"] = None

        try:
            d["Beds"] = item.find("span", {"class", "infoBed"}).find("b").text
        except:
            d["Beds"] = None

        try:
            d["Full Bath"] = item.find("span", {"class", "infoValueFullBath"}).find("b").text
        except:
            d["Full Bath"] = None

        try:
            d["Half Bath"] = item.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except:
            d["Half Bath"] = None

        try:
            d["SqFt"] = item.find("span", {"class", "infoSqFt"}).find("b").text
        except:
            d["SqFt"] = None

        for column_group in item.find_all("div", {"class": "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("spans", {"class": "featureGroup"}), column_group.find_all("span", {"class": "featureName"})):
                print(feature_group.text, feature_name.text)
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        l.append(d)

df.to_csv("PropertyInfo.Csv")
