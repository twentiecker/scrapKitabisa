import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Web scrapper for infinite scrolling page
driver = webdriver.Firefox(executable_path="D:\python\geckodriver.exe")
driver.get("https://galangdana.kitabisa.com/partners/bareng-bapau")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
scroll_height = driver.execute_script("return document.body.scrollHeight;")

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

##### Extract Reddit URLs #####
urls = []
url_temp = ""
soup = BeautifulSoup(driver.page_source, "html.parser")
for parent in soup.find_all("div"):
    try:
        a_tag = parent.find("a", class_="style__Item-okdchp-0 cusftu")
        base = "https://galangdana.kitabisa.com/partners/bareng-bapau"
        link = a_tag['href']
        url = urljoin(base, link)
        url_news = url + "/latest-news"
        if url_news != url_temp:
            urls.append(url_news)
            url_temp = url_news
    except:
        pass

print(len(urls))
print(urls)
