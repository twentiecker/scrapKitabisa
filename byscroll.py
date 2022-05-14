from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime
import sys

url = "https://galangdana.kitabisa.com/partners/bersamalawancorona"

service = ChromeService(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
# driver.get(f"{url}")
# time.sleep(2)  # Allow 2 seconds for the web page to open
# scroll_pause_time = 5  # You can set your own pause time

# # Define scrollable tag/div
# scrollable_div = driver.find_element(By.TAG_NAME, "html")
# print(scrollable_div)
# for i in range(3):
#     driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
#     time.sleep(scroll_pause_time)
#     print(f"scroll {i}")

driver = webdriver.Chrome(service=service)
driver.get(f"{url}")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 3  # You can set your own pause time
screen_height = driver.execute_script("return window.screen.height;")  # Get the screen height of the web

# Get base info from this page
page_soup = BeautifulSoup(driver.page_source, "html.parser")
x = page_soup.find("ul", {"class": "partner-avatar__list list-nostyle"})
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
    page_soup = BeautifulSoup(driver.page_source, "html.parser")
    items = page_soup.find_all("div", class_="m-card")

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
        page_soup = BeautifulSoup(driver.page_source, "html.parser")
        items = page_soup.find_all("div", class_="m-card")

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