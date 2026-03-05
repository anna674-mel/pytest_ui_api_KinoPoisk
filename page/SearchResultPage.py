from configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SearchResultPage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(
            browser, ConfigProvider().get_ui_waiting_time()
        )

    def is_empty_result_search(self):
        text = "К сожалению, по вашему запросу ничего не найдено..."
        item = (By.CSS_SELECTOR, ".textorangebig")
        elem = self.wait.until(EC.presence_of_element_located(item))
        return text == elem.text
