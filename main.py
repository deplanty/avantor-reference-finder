import time
from typing import Any
import webbrowser

import toml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Application:
    def __init__(self):
        # List of all the URL to open
        self.all_url: list[str] = list()

        # Get config
        self.config: dict[str, Any] = toml.load("config.toml")

        # Load the cache
        self.cache: dict[str, str] = toml.load("cache.toml")

        # The selenium driver used to retreive the URL to open
        self.driver = webdriver.Chrome()
        self.driver_wait = WebDriverWait(self.driver, 30)

        # Open the web site
        self.driver.get(self.config["webpage"])

    def get_url(self, reference: str):
        """Get the URL for the reference.
        Get the URL from the cache file or find it on the website.
        Store the URL in the variable `all_url`.

        Args:
            reference (str): The reference number of the product.
        """

        if reference in self.cache:
            url = self.cache[reference]
        else:
            url = self.find_url(reference)
            self.cache[reference] = url
        self.all_url.append(url)

    def find_url(self, reference: str) -> str:
        # Get the search engine application
        search_app = self.driver_wait.until(EC.presence_of_element_located((By.TAG_NAME, "app-avtr-search-box")))

        # Activate the application by clicking on it and wait for it to load
        search_bar = search_app.find_element(By.CLASS_NAME, "searchbox")
        search_bar.click()

        # Add the reference in the input text
        search_input = self.driver_wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))

        # search_input = search_bar.find_element(By.TAG_NAME, "input")
        search_input.send_keys(reference)
        time.sleep(1)

        # Find the first link in the result bar and click on it
        # results = search_app.find_elements(By.CLASS_NAME, "underline-text")
        result = self.driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.underline-text")))
        result.click()

        # Wait some time for the page to load and get the URL
        time.sleep(self.config["delay_get_url"])
        return self.driver.current_url

    def open_all_url(self):
        for url in self.all_url:
            webbrowser.open_new_tab(url)

    def save_cache(self):
        with open("cache.toml", "w", encoding="utf-8") as fid:
            toml.dump(self.cache, fid)


if __name__ == "__main__":
    # Read all the references to get
    with open("references.txt", encoding="utf-8") as fid:
        references = list()
        for line in fid:
            line = line.rstrip()
            if line:
                references.append(line)

    app = Application()
    for reference in references:
        app.get_url(reference)
    app.open_all_url()
    app.save_cache()
