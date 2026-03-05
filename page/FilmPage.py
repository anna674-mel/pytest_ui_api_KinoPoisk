from configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class FilmPage():
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(
            browser, ConfigProvider().get_ui_waiting_time()
        )
        self.movie_titles = (By.CSS_SELECTOR, "h1[itemprop='name'] span")

    def get_movie_title(self):
        return self.wait.until(
            EC.presence_of_element_located(self.movie_titles)
        )
