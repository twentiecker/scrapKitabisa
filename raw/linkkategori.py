# scrap link katalog kitabisa dan menulisnya dalam file csv

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

kategori = [
    "balita-anak-sakit",
    "bantuan-medis",
    "beasiswa-pendidikan",
    "bencana-alam",
    "difabel",
    "hewan",
    "infrastruktur",
    "karya-kreatif",
    "kegiatan-sosial",
    "kemanusiaan",
    "lingkungan",
    "panti-asuhan",
    "rumah-ibadah",
    "run-charity",
    "zakat"
]

for child in kategori:
    # membuat file csv for excel dengan nama "cnbcindonesia.csv"
    filename = f"link_{child}.csv"

    # membuka file csv dengan memberikan atribut "w" yang berarti inisiasi untuk melakukan write pada file tsb
    f = open(filename, "w", encoding="utf-8")

    # menuliskan judul (headers) pada baris pertama file csv
    headers = "urls, urls_latest_news, title\n"
    f.write(headers)

    driver = webdriver.Firefox(executable_path="D:\python\geckodriver.exe")
    driver.get(f"https://kitabisa.com/explore/{child}")
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web

    scroll_max_cek = 0
    i = 10
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 10
        time.sleep(scroll_pause_time)
        scroll_max = driver.execute_script("return window.scrollMaxY;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        # if scroll_max == scroll_max_cek:
        #     break
        # scroll_max_cek = scroll_max
        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            cek = soup.find("p")
            print(cek.text)
            if cek.text == "Kamu sudah melihat semua penggalangan dana 🌟":
                break
        except:
            pass

    i = 1
    list_url = []
    list_url_latest_news = []
    list_judul = []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for parent in soup.find_all("a", class_="style__Item-okdchp-0 cusftu"):
        try:
            base = "https://kitabisa.com"
            url_part = parent['href']
            url = urljoin(base, url_part)
            url_latest_news = url + "/latest-news"
            print(f"{i}. {url_latest_news}")
            i = i + 1
            list_url.append(url)
            list_url_latest_news.append(url_latest_news)
        except:
            pass

    for parent in soup.find_all("span", class_="cardStyle__CardTitle-rjuxnd-0 pGMPs"):
        try:
            judul = parent.text.replace(",", " ").strip()
            list_judul.append(judul)
        except:
            pass

    for i in range(len(list_url)):
        f.write(list_url[i] + "," + list_url_latest_news[i] + "," + list_judul[i] + "\n")

    driver.close()
