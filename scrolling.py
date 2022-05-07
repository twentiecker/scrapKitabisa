from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
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
        driver = webdriver.Chrome(service=self.service, options=self.opts)
        driver.get(f"{url}")
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 3  # You can set your own pause time
        screen_height = driver.execute_script("return window.screen.height;")  # Get the screen height of the web

        # Get base info from this page
        self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
        x = self.page_soup.find("ul", {"class": "partner-avatar__list list-nostyle"})
        y = x.find_all("li")
        for z in y:
            campaign = z.find("span", {"class": "fa fa-users"})
            if campaign:
                temp = int(z.text.replace("Campaign", "").strip())

        i = 1
        i_temp = 1
        temp_eq = 0
        temp_eq2 = 0
        while True:
            driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)

            # Get all new item from scrolling down
            self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
            items = self.page_soup.find_all("div", class_="m-card")

            print(f"Data scraped: {len(items)}")
            print(f"Total campaigns (to scraped): {temp}")
            print(f"Scrolling count: {i}")

            # Break the loop
            # Case temp is really equal to our div collection
            if len(items) == temp:
                print("==========================================")
                print("===== Double check in progress!! =====")
                # Make sure its already in the end of page (not still in loading content)
                time.sleep(20)
                self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
                items = self.page_soup.find_all("div", class_="m-card")

                if len(items) == temp:
                    print("===== Double checked, Done!! =====")
                    print("==========================================")
                    break
                else:
                    print("===== Got another data, Continue to scrolling page!! =====")
                    continue
            # Case for temp not equal to our div collection but it was already in the end of page
            if len(items) == temp_eq:
                i_temp += 1
                temp_eq2 = temp_eq
                print("===== Attempt waiting to loaded page =====")
                print(f"Re-attempt: {i_temp - 1}")
                if i_temp == 30:
                    print("===== Page is fully loaded, Done!! =====")
                    break
            temp_eq = len(items)

            # Check Re-attempt system
            if temp_eq2 != temp_eq:
                i_temp = 1

            print("==========================================")
        driver.close()

    def scroll_detail(self, url_detail):
        driver = webdriver.Chrome(service=self.service, options=self.opts)
        driver.get(url_detail)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 3  # You can set your own pause time
        screen_height = driver.execute_script("return window.screen.height;")  # Get the screen height of the web

        i = 1
        flag = True
        while True:
            # Scroll one screen height each time
            driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            # Update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")

            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if screen_height * i > scroll_height:
                break

            # Break the loop when content a specified word (in this case is "tahun")
            self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
            reference = self.page_soup.find_all(class_="style__UpdateTime-sc-__sc-bl8jwv-8 lnbfOR")
            for x in reference:
                if "tahun" in x.text:
                    flag = False
                    break
            if not flag:
                break

        self.page_soup_detail = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()

    def scroll_donor(self, url_donor):
        driver = webdriver.Chrome(service=self.service, options=self.opts)
        driver.get(url_donor)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 3  # You can set your own pause time

        if driver.current_url != url_donor:
            self.validate_url = False
            driver.close()
        else:
            screen_height = driver.execute_script("return window.screen.height;")  # Get the screen height of the web

            i = 1
            flag = True
            month_dic = {"Januari": "1", "Februari": "2", "Maret": "3", "April": "4", "Mei": "5", "Juni": "6",
                         "Juli": "7",
                         "Agustus": "8", "September": "9", "Oktober": "10", "November": "11", "Desember": "12"}
            now = datetime.datetime.now()
            while True:
                # Scroll one screen height each time
                driver.execute_script(
                    "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                time.sleep(scroll_pause_time)

                # Update scroll height each time after scrolled, as the scroll height can change
                # after we scrolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")

                # Break the loop when the height we need to scroll to is larger than the total scroll height
                if screen_height * i > scroll_height:
                    if i == 1:
                        sys.stdout.write(f"\r===== Nothing to Scroll =====")
                        sys.stdout.flush()
                    break

                # Break the loop when content a specified word (in this case is "one year from now")
                self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
                reference = self.page_soup.find_all(class_="style__DonationTime-sc-__sc-1exee2-9 kBDzcm")
                if reference:
                    for x in reference:
                        date = x.text
                        tahun = int(date.split(sep=" ")[2])

                        split_date = date.split(sep=" ")
                        scrap_date = "/".join(split_date[0:3])
                        modify_date = scrap_date.replace(" ", "/").replace(date.split(sep=" ")[1],
                                                                           month_dic[date.split(sep=" ")[1]])
                        convert_date = datetime.datetime.strptime(modify_date, "%d/%m/%Y")
                        delta_date = now - convert_date

                        sys.stdout.write(f"\r===== Scrolling {i} ({delta_date.days} days) =====")
                        sys.stdout.flush()

                        if (delta_date.days >= 365 and tahun % 4 == 0) or (delta_date.days >= 366 and tahun % 4 != 0):
                            flag = False
                            break
                    if not flag:
                        break

                    i += 1
                else:
                    sys.stdout.write(f"\r===== Blank Page =====")
                    sys.stdout.flush()
                    break

            self.page_soup_donor = BeautifulSoup(driver.page_source, "html.parser")
            self.validate_url = True
            driver.close()
