from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome("C:/Users/home/Desktop/desktop data/PRO-C127-Reference-Code-main/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

planets_data = []

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"
           ]

def scrape():
    for i in range(1,5):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Check page number    
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            # Get Hyperlink Tag
            hyperlink_li_tag = li_tags[0]

            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            planets_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")


# Calling Method
scrape()


new_planets_data = []

#create scrape more data function
def scrapmoredata(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        templist = []
        for tr_tag in soup.find_all("tr", attrs = {"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    templist.append(td_tag.find_all("div", attrs = {"class" : "value"})[0].contents[0])
                except:
                    templist.append("")
        new_planets_data.append(templist)
    except:
        time.sleep(1)
        scrapmoredata(hyperlink)
for index, data in enumerate(planets_data):
    scrapmoredata(data[5])
    print(f"scraping at hyperlink {index +1} is completed")
final_planet_data = []
print(new_planets_data[0:10])
with open("final.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)
#Calling method





