from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
import datetime
import sys


class Scrolling:
    def __init__(self):
        self.service = ChromeService(executable_path=ChromeDriverManager().install())
        self.opts = Options()
        self.opts.add_argument("--headless")
        self.opts.add_argument("--no-sandbox")
        self.opts.add_argument("--window-size=1420,1080")
        self.opts.add_argument("--disable-gpu")
        self.opts.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")

        self.page_soup = ""
        self.page_soup_detail = ""
        self.page_soup_donor = ""
        self.validate_url = True

    def scroll(self, url):
        driver = uc.Chrome(use_subprocess=True)
        driver.get(f"{url}")
        time.sleep(3)  # Allow 3 seconds for the web page to open
        scroll_pause_time = 6  # You can set your own pause time

        # Get initial info from this page
        self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
        x = self.page_soup.find("ul", {"class": "partner-avatar__list list-nostyle"})
        y = x.find_all("li")
        for z in y:
            campaign = z.find("span", {"class": "fa fa-users"})
            if campaign:
                temp = int(z.text.replace("Campaign", "").strip())

        # Define scrollable tag/div
        scrollable_div = driver.find_element(By.TAG_NAME, "html")

        i = 1
        i_temp = 1
        temp_eq = 0
        temp_eq2 = 0

        while True:
            # Scroll to the bottom
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(scroll_pause_time)

            # Get all new item from scrolling down
            self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
            items = self.page_soup.find_all("div", class_="m-card")

            print(f"Data Scraped: {len(items)}")
            print(f"Total Campaigns (to Scraped): {temp}")
            print(f"Scrolling Count: {i}")

            # Break the loop when temp is really equal to our div collection
            if len(items) == temp:
                print("==========================================")
                print("===== Double Check in Progress!! =====")
                # Make sure its already in the end of page (not still in loading content)
                time.sleep(20)
                self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
                items = self.page_soup.find_all("div", class_="m-card")

                if len(items) == temp:
                    print("===== Double Check is Done!! =====")
                    print("==========================================")
                    break
                else:
                    print("===== Got Another Data, Continue to Scrolling Page!! =====")
                    continue

            # Break the loop when temp not equal to our div collection but it was already in the end of page
            if len(items) == temp_eq:
                i_temp += 1
                temp_eq2 = temp_eq
                print("===== Attempt Waiting to Load Page =====")
                print(f"Re-Attempt: {i_temp - 1}")
                if i_temp == 10:
                    print("===== Page is Fully Loaded, Done!! =====")
                    break
            temp_eq = len(items)

            # Check Re-attempt system
            if temp_eq2 != temp_eq:
                i_temp = 1

            print("==========================================")
            i += 1
        driver.close()

    def scroll_detail(self, url_detail):
        driver = webdriver.Chrome(service=self.service, options=self.opts)
        driver.get(url_detail)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 6  # You can set your own pause time

        if driver.current_url != url_detail:
            self.validate_url = False
            print("===== Wrong Url!! =====")
            driver.close()
        else:
            # Define scrollable tag/div
            scrollable_div = driver.find_element(By.TAG_NAME, "html")

            scroll_height_verify = 0
            i = 1
            flag = True

            while True:
                # Scroll to the bottom
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                time.sleep(scroll_pause_time)

                # Update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")

                # Break the loop when content a specified date (in this case is "one year from scraping date")
                self.page_soup_detail = BeautifulSoup(driver.page_source, "html.parser")
                reference = self.page_soup_detail.find_all(class_="style__UpdateTime-sc-__sc-bl8jwv-8")
                if reference:
                    for x in reference:
                        sys.stdout.write(f"\r===== Scrolling Count: {i} ({x.text}) =====")
                        sys.stdout.flush()

                        # Break the loop when find word "tahun"
                        if "tahun" in x.text:
                            flag = False
                            sys.stdout.write(f"\n===== Date limit Reached =====")
                            sys.stdout.flush()
                            break
                    if not flag:
                        break

                    i += 1
                else:
                    sys.stdout.write("\r===== Blank Page =====")
                    sys.stdout.flush()
                    break

                # Break the loop when the height is not increasing anymore
                if scroll_height_verify == scroll_height:
                    time.sleep(20)
                    scroll_height = driver.execute_script("return document.body.scrollHeight;")
                    if scroll_height_verify == scroll_height:
                        sys.stdout.write(f"\n===== Bottom Page Reached =====")
                        sys.stdout.flush()
                        break
                    else:
                        print("\n===== Got Another Data, Continue to Scrolling Page!! =====")
                        continue

                scroll_height_verify = scroll_height
            self.validate_url = True
            driver.close()

    def scroll_donor(self, url_donor):
        driver = webdriver.Chrome(service=self.service, options=self.opts)
        driver.get(url_donor)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 6  # You can set your own pause time

        if driver.current_url != url_donor:
            self.validate_url = False
            print("===== Wrong Url!! =====")
            driver.close()
        else:
            # Define scrollable tag/div
            scrollable_div = driver.find_element(By.TAG_NAME, "html")

            scroll_height_verify = 0
            i = 1
            flag = True

            now = datetime.datetime.now()
            month_dic = {"Januari": "1", "Februari": "2", "Maret": "3", "April": "4", "Mei": "5", "Juni": "6",
                         "Juli": "7", "Agustus": "8", "September": "9", "Oktober": "10", "November": "11",
                         "Desember": "12"}

            while True:
                # Scroll to the bottom
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                time.sleep(scroll_pause_time)

                # Update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")

                # Break the loop when content a specified date (in this case is "one year from scraping date")
                self.page_soup_donor = BeautifulSoup(driver.page_source, "html.parser")
                reference = self.page_soup_donor.find_all(class_="style__DonationTime-sc-__sc-1exee2-9")
                if reference:
                    for x in reference:
                        date = x.text
                        tahun = int(date.split(sep=" ")[2])

                        split_date = date.split(sep=" ")
                        scrap_date = "/".join(split_date[0:3])
                        modify_date = scrap_date.replace(" ", "/") \
                            .replace(date.split(sep=" ")[1], month_dic[date.split(sep=" ")[1]])
                        convert_date = datetime.datetime.strptime(modify_date, "%d/%m/%Y")
                        delta_date = now - convert_date

                        sys.stdout.write(f"\r===== Scrolling Count: {i} ({delta_date.days} days) =====")
                        sys.stdout.flush()

                        # Break the loop when difference date more than 365 or 366 (depend on "kabisat year" or not)
                        if (delta_date.days >= 365 and tahun % 4 == 0) or (delta_date.days >= 366 and tahun % 4 != 0):
                            flag = False
                            sys.stdout.write(f"\n===== Date limit Reached =====")
                            sys.stdout.flush()
                            break
                    if not flag:
                        break

                    i += 1
                else:
                    sys.stdout.write(f"\r===== Blank Page =====")
                    sys.stdout.flush()
                    break

                # Break the loop when the height is not increasing anymore
                if scroll_height_verify == scroll_height:
                    time.sleep(20)
                    scroll_height = driver.execute_script("return document.body.scrollHeight;")
                    if scroll_height_verify == scroll_height:
                        sys.stdout.write(f"\n===== Bottom Page Reached =====")
                        sys.stdout.flush()
                        break
                    else:
                        print("\n===== Got Another Data, Continue to Scrolling Page!! =====")
                        continue

                scroll_height_verify = scroll_height
            self.validate_url = True
            driver.close()
