import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    
    yield driver

    driver.quit()


def test_show_all_pets(driver):
    # Устанавливаем явное ожидание
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('naruto_moto@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('310906')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

def test_my_photos(driver):
    driver.find_element(By.ID, 'email').send_keys('naruto_moto@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('310906')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(1)
    button = driver.find_element(By.LINK_TEXT, "Мои питомцы")
    button.click()

    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    image_count = driver.find_elements(By.XPATH,'//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/th[1]/img[1]')
    assert len(image_count) >= len(pets_count) / 2

def test_my_pets_name_age_breed(driver):
    driver.find_element(By.ID, 'email').send_keys('naruto_moto@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('310906')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(3)
    button = driver.find_element(By.LINK_TEXT, "Мои питомцы")
    button.click()

    # Установиливаем неявное ожидание
    driver.implicitly_wait(10)
    driver.find_element(By.ID, "all_my_pets")

    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[2]')
    breeds = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[3]')
    ages = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[4]')

    for i in range(len(names)):
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''

def test_my_pets_no_same_names(driver):
    driver.find_element(By.ID, 'email').send_keys('naruto_moto@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('310906')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(3)
    button = driver.find_element(By.LINK_TEXT, "Мои питомцы")
    button.click()

    all_rows = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')
    pet_names = []

    for row in all_rows:
        name_element = row.find_element(By.TAG_NAME, 'td')

        pet_names.append(name_element.text)
        unique_names = set(pet_names)
        assert len(unique_names) == len(pet_names)