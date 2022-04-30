from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

# membuat file csv for excel dengan nama "cnbcindonesia.csv"
filename = "link_covid19.csv"

# membuka file csv dengan memberikan atribut "w" yang berarti inisiasi untuk melakukan write pada file tsb
f = open(filename, "w", encoding="utf-8")

# menuliskan judul (headers) pada baris pertama file csv
headers = "url\n"
f.write(headers)

driver = webdriver.Firefox(executable_path="D:\python\geckodriver.exe")
driver.get("https://galangdana.kitabisa.com/partners/bersamalawancorona")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web

i = 10
urls = []
pattern = r"\s+"
scroll_max_cek = 0

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 10
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_max = driver.execute_script("return window.scrollMaxY;")
    if scroll_max == scroll_max_cek:
        break
    scroll_max_cek = scroll_max

soup = BeautifulSoup(driver.page_source, "html.parser")
for parent in soup.find_all("a", class_="m-card__href"):
    try:
        url = parent['href']
        url_latest_news = re.sub(pattern, "", url) + "/latest-news"
        urls.append(url_latest_news)
    except:
        pass

print(len(urls))
print(urls)

for j in range(len(urls)):
    f.write(urls[j] + "\n")
