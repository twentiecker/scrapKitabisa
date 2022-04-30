# simulasi dengan 4 kali scroll

import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Web scrapper for infinite scrolling page (katalog kitabisa)
driver = webdriver.Firefox(executable_path="D:\python\geckodriver.exe")
driver.get("https://kitabisa.com/orang-baik/343d5169b3f5b14d902c8b6a89656957")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web

i = 1
while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) + ((i - 1) * 3) > scroll_height:
        # if (screen_height) * i > scroll_height:
        break

##### Extract Reddit URLs #####
urls = []
url_temp = ""
soup = BeautifulSoup(driver.page_source, "html.parser")
for parent in soup.find_all("div"):
    try:
        a_tag = parent.find("a", class_="style__Item-okdchp-0 cusftu")
        base = "https://kitabisa.com/orang-baik/343d5169b3f5b14d902c8b6a89656957"
        link = a_tag['href']
        url = urljoin(base, link)
        url_news = url + "/latest-news"
        if url_news != url_temp:
            urls.append(url_news)
            url_temp = url_news
    except:
        pass

# print(len(urls))
driver.close()

list_title = []
for url in urls:
    # Web scrapper for infinite scrolling page
    driver = webdriver.Firefox(executable_path="D:\python\geckodriver.exe")
    driver.get(url)
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web

    i = 1
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

    ##### Extract kitabisa content #####
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for parent in soup.find_all(class_="style__UpdateContent-bl8jwv-9 goRGVn"):
        title_tag = parent.find("h4")
        list_title.append(title_tag.text)

    driver.close()

print(len(list_title))
print(list_title)
