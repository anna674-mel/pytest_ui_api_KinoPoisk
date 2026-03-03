from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure


@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver


@pytest.fixture(scope="module")
def search_input():
    return (By.CSS_SELECTOR, ".kinopoisk-header-search-form-input__input")


@pytest.mark.ui
@allure.title("Поиск фильма по валидному названию")
def test_search_movie_by_text(browser, search_input):
    text = "Брат"
    browser.get(ConfigProvider().get_ui_url())
    wait = WebDriverWait(browser, ConfigProvider().get_ui_waiting_time())
    search_input = wait.until(EC.presence_of_element_located(search_input))
    search_input.send_keys(text)
    wait.until(EC.presence_of_element_located((By.ID, "suggest-container")))
    top_result = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ul[role='list'] li[data-index='0']"))
    )
    wait.until(EC.element_to_be_clickable(top_result))
    element = browser.find_element(
        By.CSS_SELECTOR, "ul[role='list'] li[data-index='0'] a"
    )
    assert text == element.text


@pytest.mark.ui
@allure.title("Переход на карточку фильма из результов поиска")
def test_go_to_movie_card(browser, search_input):
    text = "Брат"
    browser.get(ConfigProvider().get_ui_url())
    wait = WebDriverWait(browser, ConfigProvider().get_ui_waiting_time())
    search_input = wait.until(EC.presence_of_element_located(search_input))
    search_input.send_keys(text)
    wait.until(EC.presence_of_element_located((By.ID, "suggest-container")))
    top_result = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul[role='list'] li[data-index='0']")
        )
    )
    top_result.click()
    movie_titles = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1[itemprop='name'] span")
        )
    )
    assert text in movie_titles.text


@pytest.mark.ui
@allure.title("Поиск фильма по не существующему названию #@%")
def test_search_not_exists_movie_name(browser, search_input):
    browser.get(ConfigProvider().get_ui_url())
    wait = WebDriverWait(browser, ConfigProvider().get_ui_waiting_time())
    search_input = wait.until(EC.presence_of_element_located(search_input))
    search_input.send_keys("#@%")
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[text()='По вашему запросу ничего не найдено']")
        )
    )


@pytest.mark.ui
@allure.title("Переход на страницу Билеты в кино из бокового меню")
def test_go_to_page_tickets(browser):
    text = "Билеты в кино"
    browser.get(ConfigProvider().get_ui_url())
    wait = WebDriverWait(browser, ConfigProvider().get_ui_waiting_time())
    item_movie_tickets = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href='/lists/movies/movies-in-cinema/']")
        )
    )
    assert text in item_movie_tickets.text
    wait.until(EC.element_to_be_clickable(item_movie_tickets))
    item_movie_tickets.click()
    title = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "main h1"))
    )
    assert text == title.text


@pytest.mark.ui
@allure.title("Поиск фильма состоящий только из пробелов")
def test_search_movie_with_whitespace(browser, search_input):
    text = "  "
    text_message = "К сожалению, по вашему запросу ничего не найдено..."
    browser.get(ConfigProvider().get_ui_url())
    wait = WebDriverWait(browser, ConfigProvider().get_ui_waiting_time())
    search_input = wait.until(EC.presence_of_element_located(search_input))
    search_input.send_keys(text)
    search_input.send_keys(Keys.ENTER)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f"//h2[text()='{text_message}']")
        )
    )


@pytest.mark.ui
@allure.title("Поиск фильма по ПУСТОМУ названию")
def test_search_with_empty_name(browser, search_input):
    text = ""
    browser.get(ConfigProvider().get_ui_url())
    wait = WebDriverWait(browser, ConfigProvider().get_ui_waiting_time())
    search_input = wait.until(
        EC.presence_of_element_located(search_input)
    )
    search_input.send_keys(text)
    search_input.send_keys(Keys.ENTER)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".randomMovieButton"))
    )
