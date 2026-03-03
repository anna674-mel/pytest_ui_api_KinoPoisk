import requests
import pytest
from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider
import allure


@allure.step("Проверка типа контента ответа")
def assert_content_type(response):
    assert response.headers["Content-Type"] == (
        "application/json; charset=utf-8"
    )


@pytest.mark.api
@allure.story("Поиск фильмов")
@allure.title("Поиск фильма по названию")
def test_search_movies_by_title():

    title = "Брат"
    headers = {
        "x-api-key": DataProvider().get_api_key(),
        "Content-Type": "application/json"
    }

    response = requests.get(
        ConfigProvider().get_api_url() + f'movie/search?query={title}',
        headers=headers
    )

    assert response.status_code == 200
    assert_content_type(response)

    data = response.json()
    assert data["docs"][0]["name"] == title


@pytest.mark.api
@allure.story("Поиск фильмов")
@allure.title("Поиск фильма по имени режиссёра")
def test_search_movies_by_name():

    name = "ЭльдарРязанов"
    headers = {
        "x-api-key": DataProvider().get_api_key(),
        "Content-Type": "application/json"
    }

    response = requests.get(
        ConfigProvider().get_api_url() + f'person/search?query={name}',
        headers=headers
    )

    assert response.status_code == 200
    assert_content_type(response)

    data = response.json()
    assert data["docs"][0]["name"] == 'Эльдар Рязанов'


@pytest.mark.api
@allure.story("Поиск фильмов")
@allure.title("Поиск фильма по году и жанру")
def test_search_movies_by_year_and_genres():

    year = 2025
    genres = "мелодрама"
    headers = {
        "x-api-key": DataProvider().get_api_key(),
        "Content-Type": "application/json"
    }

    response = requests.get(
        ConfigProvider().get_api_url()
        + f'movie?year={year}&genres.name={genres}',
        headers=headers
    )

    assert response.status_code == 200
    assert_content_type(response)

    data = response.json()
    assert data["docs"][0]["year"] == year
    assert any(
        genre["name"] == "мелодрама" for genre in data["docs"][0]["genres"]
    )


@pytest.mark.api
@allure.story("Поиск фильмов")
@allure.title("Поиск фильма без авторизации")
def test_request_without_api_key():

    title = "Брат"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(
        ConfigProvider().get_api_url() + f'movie/search?query={title}',
        headers=headers
    )

    assert response.status_code == 401
    assert_content_type(response)

    data = response.json()
    assert data["message"] == "В запросе не указан токен!"


@pytest.mark.api
@allure.story("Поиск фильмов")
@allure.title("Номер сезона указан не в верном (не в числовом) формате")
def test_request_with_not_valid_parameter():

    headers = {
        "x-api-key": DataProvider().get_api_key(),
        "Content-Type": "application/json"
    }

    response = requests.get(
        ConfigProvider().get_api_url() + "season?movieId=F",
        headers=headers
    )

    assert response.status_code == 400
    assert_content_type(response)

    data = response.json()
    assert data["message"][0] == (
        "Поле movieId должно быть числом или массивом чисел!"
    )
