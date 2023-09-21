import requests
from bs4 import BeautifulSoup
import re
import advertools as adv

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#webscrape to get all the silly holidays per day!
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
    days.append("National Thumbs Up Bread Day")
    return days

#get the keywords of the holidays
# some nouns are 2 words... need fix
def getKeyWords():
    days = dayGenerator()
    stopwords = ['world', 'national', 'day', 'international', 'of', "’", 's', 'awareness']
    filtered_list = {}

    for day in days:
        words = word_tokenize(day)
        for w in words:
            if w.lower().strip() not in stopwords:
                #print(w)
                filtered_list[w] = day

    return filtered_list

#potentially find and emoji that corresponds to that keyword
#reutrns a dictionary with Keyword:Emoji Symbol
def getEmoji():
    words = getKeyWords()
    emoji_dict = {}
    for word in words:
        emoji = adv.emoji_search(word)
        if emoji.empty == False:
            emoji_dict[word] = emoji.iloc[0]['emoji']
    
    return emoji_dict

#update the name of the holidays to include the emoji
def updateHolidays():
    #days = dayGenerator()
    keywords = getKeyWords()
    emojis = getEmoji()

    final = []
    test = {}

   # the pecan cookie day : _ _


    for key in keywords: #{keyword: full holiday name}
        if key in emojis: #{keyword: emoji}
            if keywords[key] in test:
                test[keywords[key]] = test[keywords[key]] + " " + emojis[key] + " "
            else:
                test[keywords[key]] = emojis[key]
        else:
            test[keywords[key]] = ""
    
    for i in test:
        final.append(i + " " + test[i])

    return final
