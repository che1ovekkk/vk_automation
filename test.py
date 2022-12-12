from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from locators import *
from time import sleep
from PIL import Image, ImageChops

def open_browser(url):
    browser = webdriver.Chrome()
    browser.get(url=url)
    browser.implicitly_wait(3)
    return browser


def get_diff(img1, img2):
    image_1 = Image.open(img1).convert('RGB')
    image_2 = Image.open(img2).convert('RGB')
    diff = ImageChops.difference(image_1, image_2).getbbox()
    return diff


def test_main():
    browser = open_browser(url='https://samara.hh.ru')

    search_field = browser.find_element(By.NAME, 'text')
    search_field.send_keys('Инженер по тестированию')
    search_field.send_keys(Keys.RETURN)
    assert 'Работа инженером по тестированию в Самаре' in browser.title


def test_filters():
    browser = open_browser(url='https://samara.hh.ru/vacancies/inzhener_po_testirovaniyu')

    filters_button = browser.find_element(By.CLASS_NAME, 'bloko-icon-link')
    filters_button.click()
    browser.implicitly_wait(3)

    delete_region = browser.find_element(By.CLASS_NAME, 'bloko-tag-button')
    browser.execute_script("arguments[0].scrollIntoView();", delete_region)
    delete_region.click()

    salary = browser.find_element(By.XPATH, salary_field)
    browser.execute_script("arguments[0].scrollIntoView();", salary)
    salary.send_keys('200000')

    only_with_salary = browser.find_element(By.XPATH, only_with_salary_field)
    browser.execute_script("arguments[0].scrollIntoView();", only_with_salary)
    only_with_salary.click()

    experience = browser.find_element(By.XPATH, experience_field)
    browser.execute_script("arguments[0].scrollIntoView();", experience)
    experience.click()

    type_of_work = browser.find_element(By.XPATH, type_field)
    browser.execute_script("arguments[0].scrollIntoView();", type_of_work)
    type_of_work.click()

    remote_work = browser.find_element(By.XPATH, remote_work_field)
    browser.execute_script("arguments[0].scrollIntoView();", remote_work)
    remote_work.click()

    search_button = browser.find_element(By.XPATH, search_button_field)
    browser.execute_script("arguments[0].scrollIntoView();", search_button)
    search_button.click()
    browser.implicitly_wait(3)
    total_vacancies = browser.find_element(By.TAG_NAME, 'h1').text
    assert 'инженер по тестированию' in total_vacancies


def test_open_result():
    browser = open_browser(url=open_result_url)

    first_vacancy = browser.find_element(By.CLASS_NAME, 'serp-item__title')
    first_vacancy.click()
    browser.implicitly_wait(3)

    browser.switch_to.window(browser.window_handles[1])
    browser.maximize_window()
    sleep(3)

    apply_button = browser.find_element(By.XPATH, apply_button_field)
    apply_button.click()
    sleep(3)

    apply_email = browser.find_element(By.NAME, 'login')
    apply_email.send_keys('balykov_ms@mail.ru')
    # clicking outside so the cursor disappears
    outside = browser.find_element(By.XPATH, outside_field)
    outside.click()
    sleep(1)
    apply_whole = browser.find_element(By.XPATH, apply_whole_field)
    browser.execute_script("arguments[0].scrollIntoView();", apply_whole)
    apply_whole.screenshot('filled_apply.png')
    diff = get_diff(img1='reference.png', img2='filled_apply.png')
    assert diff is None, "Images doesn't match"


#TODO - поставить allure и попробовать намутить аллюр-отчёт
