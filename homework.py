import time

import folium as folium
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import googlemaps

driver = webdriver.Chrome('C:/Backshi/Python/Day2/chromedriver.exe')
driver.get('https://banapresso.com/store')

html = driver.page_source
soup = BeautifulSoup(html)
comment = []
pagenum = 1

while (True):
    time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html)

    content_area = soup.find_all('span', {'class', 'store_name_map'})

    for i in range(len(content_area)):
        comment1 = content_area[i].find('i').text
        comment2 = content_area[i].find('span').text
        comment.append([comment1, comment2])

    for i in range(2, 6):
        if pagenum == 4:
            driver.find_element('xpath',
                                '//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[' + pagenum + ']/span').click()
        else:
            driver.find_element('xpath', '//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[' + str(
                i) + ']/a').click()
        time.sleep(0.5)
        html = driver.page_source
        soup = BeautifulSoup(html)

        content_area = soup.find_all('span', {'class', 'store_name_map'})

        for i in range(len(content_area)):
            comment1 = content_area[i].find('i').text
            comment2 = content_area[i].find('span').text
            comment.append([comment1, comment2])
            pagenum += 1
    break
driver.find_element('xpath', '//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/span/a').click()
while (True):
    time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html)

    content_area = soup.find_all('span', {'class', 'store_name_map'})
    for i in range(len(content_area)):
        comment1 = content_area[i].find('i').text
        comment2 = content_area[i].find('span').text
        comment.append([comment1, comment2])

    for i in range(2, 5):
        if pagenum == 6:
            driver.find_element('xpath',
                                '//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[' + pagenum + ']/span').click()
        else:
            driver.find_element('xpath', '//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[' + str(
                i) + ']/a').click()
        time.sleep(0.5)
        html = driver.page_source
        soup = BeautifulSoup(html)

        content_area = soup.find_all('span', {'class', 'store_name_map'})

        for i in range(len(content_area)):
            comment1 = content_area[i].find('i').text
            comment2 = content_area[i].find('span').text
            comment.append([comment1, comment2])
            pagenum += 1
    break
print(comment)

list = pd.DataFrame(comment)
list.columns = ['지점', '주소']
list.to_csv("./bana.csv")

googlemaps_key = ""
gmaps = googlemaps.Client(key=googlemaps_key)

total = []

for i in range(len(list)):
    if i == 84:
        break
    geo_location = gmaps.geocode(list['주소'][i])[0].get('geometry')
    lat = geo_location['location']['lat']
    lng = geo_location['location']['lng']
    total.append([list['지점'][i], list['주소'][i], lat, lng])
total_list = pd.DataFrame(total)
total_list.columns = ['지점', '주소', '위도', '경도']
total_list.to_csv("./banalist.csv")
print(total_list)

total_list = pd.read_csv('banalist.csv')

data = total_list

bana_map = folium.Map(location=[data['위도'].mean(), data['경도'].mean()], zoom_start=11)

for i in data.index:
    bana_name = data.loc[i, "지점"] + ' - ' + data.loc[i, '주소']
    popup = folium.Popup(bana_name, max_width=500)
    folium.Marker(location=[data.loc[i, '위도'], data.loc[i, '경도']], popup=popup).add_to(bana_map)
bana_map.save('./bana_map.html')

