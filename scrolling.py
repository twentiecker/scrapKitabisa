from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime


class Scrolling:
    def __init__(self):
        self.service = ChromeService(executable_path=ChromeDriverManager().install())
        self.page_soup = ""
        self.page_soup_detail = ""

    def scroll(self, url):
        # service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=self.service)
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
                print("===== Double check in progress!! =====")
                # Make sure its already in the end of page (not still in loading content)
                time.sleep(20)
                self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
                items = self.page_soup.find_all("div", class_="m-card")

                if len(items) == temp:
                    print("===== Double checked, Done!! =====")
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
        # service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=self.service)
        driver.get(url_detail)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 1  # You can set your own pause time
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
            if flag == False:
                break

        self.page_soup_detail = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()

    def scroll_donor(self, url_detail):
        # service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=self.service)
        driver.get(url_detail)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 1  # You can set your own pause time
        screen_height = driver.execute_script("return window.screen.height;")  # Get the screen height of the web

        i = 1
        flag = True
        now = datetime.datetime.now().strftime("%d/%m/%Y")
        month = int(now.split(sep="/")[1])
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

            # Break the loop when meet certain reference month in current quarter (t-1)
            self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
            reference = self.page_soup.find_all(class_="style__DonationTime-sc-__sc-1exee2-9 kBDzcm")
            for x in reference:
                month_scrap = x.text.split(sep=" ")[1].strip()
                if (month - 1 >= 1) and (month - 1 <= 3):
                    month_range = "Januari, Februari, Maret"
                    if month_scrap in month_range:
                        continue
                    else:
                        flag = False
                        break
                elif (month - 1 >= 4) and (month - 1 <= 6):
                    month_range = "April, Mei, Juni"
                    if month_scrap in month_range:
                        continue
                    else:
                        flag = False
                        break
                elif (month - 1 >= 7) and (month - 1 <= 9):
                    month_range = "Juli, Agustus, September"
                    if month_scrap in month_range:
                        continue
                    else:
                        flag = False
                        break
                elif (month - 1 >= 10) and (month - 1 <= 12):
                    month_range = "Oktober, November, Desember"
                    if month_scrap in month_range:
                        continue
                    else:
                        flag = False
                        break
            if flag == False:
                break

        self.page_soup_detail = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
