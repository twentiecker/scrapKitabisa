import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

kategori = [
    # "balita-anak-sakit",
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

for data_kategori in kategori:
    urls = []
    judul = []
    with open(f"link_{data_kategori}.csv", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                print(row[0])
                urls.append(row[0])
                judul.append(row[2])
                line_count += 1
        # print(f'Processed {line_count} lines.')
        print(len(urls))
        # print(urls

    list_judul = []
    list_time = []
    list_donasi = []
    list_update_time = []
    list_url_scrapping = []

    # membuat file csv for excel dengan nama "cnbcindonesia.csv"
    filename = f"kitabisa_donasi_{data_kategori}.csv"

    # membuka file csv dengan memberikan atribut "w" yang berarti inisiasi untuk melakukan write pada file tsb
    f = open(filename, "w", encoding="utf-8")

    # menuliskan judul (headers) pada baris pertama file csv
    headers = "scrap_date, date, fund, url\n"
    f.write(headers)

    x = 1
    for parent in urls:
        url = parent + "/donors";
        print(f"{x}. {url}")
        # infinite scrolling
        driver = webdriver.Firefox(executable_path="D:\python\geckodriver.exe")
        driver.get(url)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
        # scroll_height = driver.execute_script("return document.body.scrollHeight;")

        i = 1
        while True:
            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height_cek = driver.execute_script("return document.body.scrollHeight;")

            # try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            cek = soup.find("div", class_="style__SpinnerWrapper-sc-104vtmk-0 ikXlYc")
            # print(cek)
            if cek is None:
                break

        # ambil data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for donasi in soup.find_all("span", class_="style__DonationAmount-sc-1exee2-8 Lcjbj"):
            # print(donasi.text.replace("Rp", "").replace(".", "").strip())
            list_donasi.append(donasi.text.replace("Rp", "").replace(".", "").strip())
            list_time.append(datetime.datetime.now().strftime("%d/%m/%Y; %H:%M:%S"))
            list_judul.append(judul[x - 1])
            list_url_scrapping.append(url)
        for update_time in soup.find_all("span", class_="style__DonationTime-sc-1exee2-9 eGPNbw"):
            # print(update_time.text.strip())
            list_update_time.append(update_time.text.strip())

        driver.close()

        for i in range(len(list_update_time)):
            # menuliskan hasil scraping ke dalam file csv yang sudah kita buat sebelumnya
            f.write(
                list_time[i] + "," + list_update_time[i] + "," + str(list_donasi[i]) + "," + str(list_judul[i]) + "," + list_url_scrapping[i] + "\n")

        x = x + 1
        list_judul = []
        list_time = []
        list_donasi = []
        list_update_time = []
        list_url_scrapping = []

    print(f"{x - 1} dari {len(urls)} link telah selesai discrapping")
