import requests
from bs4 import BeautifulSoup

def dayGenerator():
    URL = 'https://www.holidaycalendar.io/what-holiday-is-today'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    result = soup.find_all("div", class_="collection-item-2 w-dyn-item")

    days = []

    for a in result:
        name = a.find("h3", class_="card-link-title---hover-secondary-1 display-4 mg-bottom-2px")
        if "Day" in name.text:
            days.append(name.text)
            #print(name.text) 

    #print(days)
    return days