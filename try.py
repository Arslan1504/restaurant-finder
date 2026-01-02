from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# 1️⃣ Open Google Maps
driver.get("https://www.google.com/maps")
time.sleep(5)

# 2️⃣ Search query
query = "istanbul restaurant"
search_box = driver.find_element(By.ID, "searchboxinput")
search_box.send_keys(query)
search_box.send_keys(Keys.ENTER)

# 3️⃣ Get place list
places = driver.find_elements(By.CLASS_NAME, "hfpxzc")
print("Found places:", len(places))

data = []

for i in range(min(10, len(places))):  # limit for safety
    places[i].click()
  
    try:
        name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
    except:
        name = None

    try:
        rating = driver.find_element(By.CLASS_NAME, "F7nice").text
    except:
        rating = None

    try:
        address = driver.find_element(By.XPATH, "//button[@data-item-id='address']").text
    except:
        address = None

    try:
        phone = driver.find_element(By.XPATH, "//button[contains(@data-item-id,'phone')]").text
    except:
        phone = None

    try:
        website = driver.find_element(By.XPATH, "//a[contains(@data-item-id,'authority')]").get_attribute("href")
    except:
        website = None

    data.append({
        "name": name,
        "rating": rating,
        "address": address,
        "phone": phone,
        "website": website
    })

    driver.back()
    time.sleep(1)

for d in data:
    print(d)

driver.quit()
from selenium.webdriver.common.action_chains import ActionChains

max_places = 10

for i in range(max_places):


    # 🔁 RE-FIND places every time (THIS FIXES STALE ERROR)
    places = driver.find_elements(By.CLASS_NAME, "hfpxzc")

    if i >= len(places):
        break

    # Scroll element into view
    driver.execute_script("arguments[0].scrollIntoView();", places[i])
    time.sleep(1)

    # Click using JS (more reliable than .click())
    driver.execute_script("arguments[0].click();", places[i])
    time.sleep(5)

    try:
        name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
    except:
        name = None

    try:
        rating = driver.find_element(By.CLASS_NAME, "F7nice").text
    except:
        rating = None

    try:
        address = driver.find_element(By.XPATH, "//button[@data-item-id='address']").text
    except:
        address = None

    try:
        phone = driver.find_element(By.XPATH, "//button[contains(@data-item-id,'phone')]").text
    except:
        phone = None

    try:
        website = driver.find_element(By.XPATH, "//a[contains(@data-item-id,'authority')]").get_attribute("href")
    except:
        website = None

    data.append({
        "name": name,
        "rating": rating,
        "address": address,
        "phone": phone,
        "website": website
    })

    # 🔙 Go back to results list
    driver.back()

