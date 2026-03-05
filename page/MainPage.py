from configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(
            browser, ConfigProvider().get_ui_waiting_time()
        )
        self.search_input = (
            By.CSS_SELECTOR, ".kinopoisk-header-search-form-input__input"
        )
        self.top_result = (
            By.CSS_SELECTOR, "ul[role='list'] li[data-index='0']"
        )
        self.suggest_container = (By.ID, "suggest-container")

    def open(self):
        self.browser.get(ConfigProvider().get_ui_url())

    def search_in_search_bar(self, text):
        search_input = self.wait.until(
            EC.presence_of_element_located(self.search_input)
        )
        search_input.send_keys(text)

    def get_first_result(self):
        self.wait.until(EC.presence_of_element_located(self.suggest_container))
        return self.wait.until(EC.presence_of_element_located(self.top_result))

    def check_element_to_be_clickable(self, element):
        self.wait.until(EC.element_to_be_clickable(element))

    def get_text_element(self, element):
        return element.find_element(By.CSS_SELECTOR, "a").text

    def go_to_film_page(self, element):
        element.click()

    def is_empty_result_search(self):
        text = "По вашему запросу ничего не найдено"
        suggest_container = self.wait.until(
            EC.presence_of_element_located(self.suggest_container)
        )
        empty_message = suggest_container.find_element(
            By.XPATH, f".//div[contains(text(), '{text}')]"
        )
        return empty_message.is_displayed()

    def go_to_movie_tickets_page(self):
        item = (By.CSS_SELECTOR, "a[href='/lists/movies/movies-in-cinema/']")
        result = self.wait.until(EC.presence_of_element_located(item))
        self.wait.until(EC.element_to_be_clickable(result))
        result.click()
