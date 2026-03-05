from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.common.keys import Keys
import allure
from page.MainPage import MainPage
from page.FilmPage import FilmPage
from page.MovieTicketsPage import MovieTicketsPage
from page.SearchResultPage import SearchResultPage
from page.ChancePage import ChancePage


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
    main_page = MainPage(browser)
    main_page.open()
    main_page.search_in_search_bar(text)
    reslult = main_page.get_first_result()
    main_page.check_element_to_be_clickable(reslult)
    title = main_page.get_text_element(reslult)
    assert text == title


@pytest.mark.ui
@allure.title("Переход на карточку фильма из результов поиска")
def test_go_to_movie_card(browser, search_input):
    text = "Брат"
    main_page = MainPage(browser)
    main_page.open()
    main_page.search_in_search_bar(text)
    reslult = main_page.get_first_result()
    main_page.check_element_to_be_clickable(reslult)
    main_page.go_to_film_page(reslult)
    film_page = FilmPage(browser)
    movie_title = film_page.get_movie_title()
    assert text in movie_title.text


@pytest.mark.ui
@allure.title("Поиск фильма по не существующему названию #@%")
def test_search_not_exists_movie_name(browser, search_input):
    text = "#@%"
    main_page = MainPage(browser)
    main_page.open()
    main_page.search_in_search_bar(text)
    assert main_page.is_empty_result_search()


@pytest.mark.ui
@allure.title("Переход на страницу Билеты в кино из бокового меню")
def test_go_to_page_tickets(browser):
    text = "Билеты в кино"
    main_page = MainPage(browser)
    main_page.open()
    main_page.go_to_movie_tickets_page()
    movie_tickets = MovieTicketsPage(browser)
    result = movie_tickets.get_movie_title()
    assert text == result.text


@pytest.mark.ui
@allure.title("Поиск фильма состоящий только из пробелов")
def test_search_movie_with_whitespace(browser, search_input):
    text = "  "
    main_page = MainPage(browser)
    main_page.open()
    main_page.search_in_search_bar(text)
    main_page.search_in_search_bar(Keys.ENTER)
    search_result_page = SearchResultPage(browser)
    assert search_result_page.is_empty_result_search()


@pytest.mark.ui
@allure.title("Поиск фильма по ПУСТОМУ названию")
def test_search_with_empty_name(browser, search_input):
    text = ""
    main_page = MainPage(browser)
    main_page.open()
    main_page.search_in_search_bar(text)
    main_page.search_in_search_bar(Keys.ENTER)
    chance_page = ChancePage(browser)
    assert chance_page.has_button_randomMovie()
