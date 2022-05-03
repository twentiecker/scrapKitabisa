from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as Soup
import os
import scrolling
import scraping
import summary
import writing
import reading

print("===== Start Initialize =====")
# url = "https://galangdana.kitabisa.com/partners/bersamalawancorona"  # BersamaLawanCorona
# url = "https://galangdana.kitabisa.com/partners/daruratcovid2021"  # DaruratCOVID2021
# url = "https://galangdana.kitabisa.com/partners/perempuanhadapicovid"  # PerempuanHadapiCovid
# url = "https://galangdana.kitabisa.com/partners/gogive-catalogue-home"  # GoGive catalogue home
url = "https://galangdana.kitabisa.com/partners/kickandyheroes"  # Kick Andy Heroes_detail
# url = "https://galangdana.kitabisa.com/partners/msract"  # Lets ACT Indonesia
# url = "https://galangdana.kitabisa.com/partners/millennialsberkarya"  # Millennials Berkarya - Semen Indonesia#
# url = "https://galangdana.kitabisa.com/partners/oxygenforindonesia"  # Oxygen for Indonesia
# url = "https://galangdana.kitabisa.com/partners/bisabantusesama"  # Program #BisaBantuSesama
# url = "https://galangdana.kitabisa.com/partners/ramadhan2021"  # Ramadhan Bersama Kitabisa #SalingJaga
# url = "https://galangdana.kitabisa.com/partners/zakathub"  # ZakatHub by BAZNAS

uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page_html = urlopen(uClient).read()
page_soup = Soup(page_html, "html.parser")
partner_name = page_soup.find("h2", {"class": "align-center"}).text.replace("\n", "").strip()

file_name_write = f"output/latest-news/{partner_name}"
file_name_write_url = f"output/latest-news/{partner_name}_url"
file_name_write_detail = f"output/latest-news/{partner_name}_detail"
file_name_write_url_remainder = f"output/latest-news/{partner_name}_remainder"

scroll = scrolling.Scrolling()
scrap = scraping.Scraping()
write = writing.Writing()
read = reading.Reading()

print("===== Finish Initialize =====")

if os.path.isfile(f"./{file_name_write_url_remainder}.csv"):  # Check file_name_write_url_remainder
    print("===== File Remainder Found =====")
    print("===== Start Reading Remainder =====")
    read.read(file_name_write_url_remainder)
    print("===== Finish Reading Remainder =====")

    list_url = tuple(read.list_url)
    for x in list_url:
        print(f"{x}/latest-news")
        url_detail = f"{x}/latest-news"
        print("===== Start Scrolling Detail Page =====")
        scroll.scroll_detail(url_detail)
        print("===== Finish Scrolling Detail Page =====")
        print("===== Start Scraping Detail Page =====")
        scrap.scrap_detail(scroll.page_soup_detail, url_detail)
        print("===== Finish Scraping Detail Page =====")
        print("===== Start Writing Detail Page =====")
        write.write_detail(file_name_write_detail, scrap.list_time, scrap.list_publisher_name, scrap.list_update_time,
                           scrap.list_update_content_h4, scrap.list_update_content_p, scrap.list_update_content_div,
                           scrap.list_url_scrapping)
        print("===== Finish Writing Detail Page =====")

        # Remove url that has been scraped from the list_remainder
        for url in list_url:
            if url == x:
                read.list_url.remove(url)
                break

        # Write remaining url that need to be scraped
        print("===== Start Writing Remainder =====")
        write.write_url(file_name_write_url_remainder, read.list_url)  # Remainder url
        print("===== Finish Writing Remainder =====")

    # Check whether file_name_write_url_remainder still usefull or not
    print("===== Start Checking File Remainder =====")
    read.read(file_name_write_url_remainder)
    if not read.list_url:
        os.remove(f"{file_name_write_url_remainder}.csv")
        os.remove(f"{file_name_write_url}.csv")
        print("===== All Remainder Url Has Been Scraped =====")
        print("===== Finish Checking File Remainder =====")

    # Create summary from file detail
    print("==== Scraped data =====")
    summary.Summary().summary(file_name_write_detail)

else:
    print("===== Start Scrolling =====")
    scroll.scroll(url)
    print("===== Finish Scrolling =====")
    print("===== Start Scraping =====")
    scrap.scrap(scroll.page_soup)
    print("===== Finish Scraping =====")
    print("===== Start Writing =====")
    write.write(file_name_write, scrap.list_campaign_name, scrap.list_campaign_fundriser, scrap.list_campaign_donation,
                scrap.list_campaign_url)
    write.write_url(file_name_write_url, scrap.list_campaign_url)
    print("===== Finish Writing =====")
    print("===== Start Reading =====")
    read.read(file_name_write_url)
    print("===== Finish Reading =====")

    list_url = tuple(read.list_url)
    for x in list_url:
        print(f"{x}/latest-news")
        url_detail = f"{x}/latest-news"
        print("===== Start Scrolling Detail Page =====")
        scroll.scroll_detail(url_detail)
        print("===== Finish Scrolling Detail Page =====")
        print("===== Start Scraping Detail Page =====")
        scrap.scrap_detail(scroll.page_soup_detail, url_detail)
        print("===== Finish Scraping Detail Page =====")
        print("===== Start Writing Detail Page =====")
        write.write_detail(file_name_write_detail, scrap.list_time, scrap.list_publisher_name, scrap.list_update_time,
                           scrap.list_update_content_h4, scrap.list_update_content_p, scrap.list_update_content_div,
                           scrap.list_url_scrapping)
        print("===== Finish Writing Detail Page =====")

        # Remove url that has been scraped from the list_remainder
        for url in list_url:
            if url == x:
                read.list_url.remove(url)
                break

        # Write remaining url that need to be scraped
        print("===== Start Writing Remainder =====")
        write.write_url(file_name_write_url_remainder, read.list_url)  # Remainder url
        print("===== Finish Writing Remainder =====")

    # Check whether file_name_write_url_remainder still usefull or not
    print("===== Start Checking File Remainder =====")
    read.read(file_name_write_url_remainder)
    if not read.list_url:
        os.remove(f"{file_name_write_url_remainder}.csv")
        os.remove(f"{file_name_write_url}.csv")
        print("===== All Remainder Url Has Been Scraped =====")
        print("===== Finish Checking File Remainder =====")

    # Create summary from file detail
    print("==== Scraped data =====")
    summary.Summary().summary(file_name_write_detail)
