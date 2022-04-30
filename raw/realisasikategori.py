import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

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
                print(row[1])
                urls.append(row[1])
                judul.append(row[2])
                line_count += 1
        # print(f'Processed {line_count} lines.')
        print(len(urls))
        # print(urls)

    list_judul = []
    list_time = []
    list_publisher_name = []
    list_update_time = []
    list_update_content_h4 = []
    list_update_content_p = []
    list_update_content_div = []
    list_url_scrapping = []

    # membuat file csv for excel dengan nama "cnbcindonesia.csv"
    filename = f"kitabisa_realisasi_{data_kategori}.csv"

    # membuka file csv dengan memberikan atribut "w" yang berarti inisiasi untuk melakukan write pada file tsb
    f = open(filename, "w", encoding="utf-8")

    # menuliskan judul (headers) pada baris pertama file csv
    headers = "scrap_date, fundriser, date, fund, bank_account, content, title, url\n"
    f.write(headers)

    x = 1
    for url in urls:
        print(f"{x}. {url}")
        # infinite scrolling
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

        # ambil data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for publisher_name in soup.find_all(class_="style__PublisherName-bl8jwv-7 dgWFCG"):
            # print(publisher_name.text)
            list_publisher_name.append(publisher_name.text.replace(",", "").strip())
            list_time.append(datetime.datetime.now().strftime("%d/%m/%Y; %H:%M:%S"))
            list_judul.append(judul[x-1])
            list_url_scrapping.append(url)
        for update_time in soup.find_all(class_="style__UpdateTime-bl8jwv-8 fjWXGg"):
            # print(update_time.text)
            list_update_time.append(update_time.text)
        for update_content in soup.find_all(class_="style__UpdateContent-bl8jwv-9 goRGVn"):
            h4_tag = update_content.find("h4")
            p_tag = update_content.find("p")
            div_tag = update_content.find("div")
            list_update_content_h4.append(h4_tag.text.replace("Pencairan Dana Rp ", "").replace(".", "").
                                          replace("\n", "").replace(",", " "))
            try:
                if "rekening" in p_tag.text:
                    list_update_content_p.append(p_tag.text.replace("\n", " ").replace(",", ""))
                else:
                    list_update_content_p.append("")
            except:
                list_update_content_p.append("")
            list_update_content_div.append(div_tag.text.replace("\n", " ").replace(",", ""))

        driver.close()

        for i in range(len(list_update_time)):
            # menuliskan hasil scraping ke dalam file csv yang sudah kita buat sebelumnya
            f.write(list_time[i] + "," + list_publisher_name[i] + "," + list_update_time[i] + "," +
                    list_update_content_h4[i] + "," + list_update_content_p[i] + "," + list_update_content_div[i] + "," +
                    list_judul[i] + "," + list_url_scrapping[i] + "\n")

            # print(list_publisher_name[i])
            # print(list_update_time[i])
            # print(list_update_content_h4[i])
            # print(list_update_content_p[i])
            # print(list_update_content_div[i])

        x = x + 1
        list_judul = []
        list_time = []
        list_publisher_name = []
        list_update_time = []
        list_update_content_h4 = []
        list_update_content_p = []
        list_update_content_div = []
        list_url_scrapping = []

    print(f"{x - 1} dari {len(urls)} link telah selesai discrapping")