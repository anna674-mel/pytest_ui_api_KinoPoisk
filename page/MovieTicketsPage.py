from configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MovieTicketsPage():
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(
            browser, ConfigProvider().get_ui_waiting_time()
        )
        self.title_page = (By.CSS_SELECTOR, "main h1")

    def get_movie_title(self):
        return self.wait.until(EC.presence_of_element_located(self.title_page))
