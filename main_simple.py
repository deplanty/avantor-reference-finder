import time
import webbrowser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


webpage = "https://www.avantorsciences.com/fr/fr/"

references = [
    "APOSOR302273-5G",
    "ACRO117150050",
    "ACRO188150100",
]

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)
driver.get(webpage)

all_url = list()

for reference in references:
    # Get the search engine application
    search_app = wait.until(EC.presence_of_element_located((By.TAG_NAME, "app-avtr-search-box")))

    # Activate the application by clicking on it and wait for it to load
    search_bar = search_app.find_element(By.CLASS_NAME, "searchbox")
    search_bar.click()

    # Add the reference in the input text
    search_input = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    print("---", search_input)

    # search_input = search_bar.find_element(By.TAG_NAME, "input")
    search_input.send_keys(reference)
    time.sleep(1)

    # Find the first link in the result bar and click on it
    # results = search_app.find_elements(By.CLASS_NAME, "underline-text")
    result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.underline-text")))
    result.click()

    # Wait some time for the page to load and get the URL
    time.sleep(10)
    all_url.append(driver.current_url)

driver.quit()

print(*all_url, sep="\n")

for url in all_url:
    webbrowser.open_new_tab(url)