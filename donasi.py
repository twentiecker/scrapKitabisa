import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as Soup
import os
import scrolling
import scraping
import summary
import writing
import reading


class Donasi:
    def scrap_donasi(self):
        list_url = tuple(read.list_url)
        for x in list_url:
            print(f"{x}/donors")
            url_donor = f"{x}/donors"
            print("===== Start Scrolling Donor Page =====")
            scroll.scroll_donor(url_donor)
            if scroll.validate_url:
                print("\n===== Finish Scrolling Donor Page =====")
                print("===== Start Scraping Donor Page =====")
                scrap.scrap_donor(scroll.page_soup_donor, url_donor)
                print("===== Finish Scraping Donor Page =====")
                print("===== Start Writing Donor Page =====")
                write.write_donor(file_name_write_donor, scrap.list_scrap_time, scrap.list_donatur, scrap.list_donasi,
                                  scrap.list_donor_time, scrap.list_url_donor)
                print("===== Finish Writing Donor Page =====")
            else:
                print("===== Finish Scrolling Donor Page =====")

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

        # Create summary from file donor
        print("===== Start Summarizing data =====")
        summary.Summary().summary_donor(file_name_write_donor)
        print("===== Finish Summarizing data =====")


url = input("Masukkan link url kitabisa partners yang akan di scraping: ")

start = time.time()
print("===== Start Initialize =====")
uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page_html = urlopen(uClient).read()
page_soup = Soup(page_html, "html.parser")
partner_name = page_soup.find("h2", {"class": "align-center"}).text.replace("\n", "").strip()

file_name_write = f"output/donasi/{partner_name}"
file_name_write_url = f"output/donasi/{partner_name}_url"
file_name_write_donor = f"output/donasi/{partner_name}_donor"
file_name_write_url_remainder = f"output/donasi/{partner_name}_remainder"

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

    Donasi().scrap_donasi()

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

    Donasi().scrap_donasi()

end = time.time()
print(f"===== Elapsed time {time.strftime('%H:%M:%S', time.gmtime(end - start))} =====")
print("===== Scraping data done!! =====")
