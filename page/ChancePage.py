from configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ChancePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(
            browser, ConfigProvider().get_ui_waiting_time()
        )

    def has_button_randomMovie(self):
        item = (By.CSS_SELECTOR, ".randomMovie")
        self.wait.until(EC.presence_of_element_located(item))
        return True
