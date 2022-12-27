from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from locators import *
from time import sleep
from PIL import Image, ImageChops
import allure


@allure.step('Открываем браузер')
def open_browser(url):
    browser = webdriver.Chrome()
    browser.get(url=url)
    browser.implicitly_wait(3)
    return browser


@allure.step('Сравниваем скриншот с эталоном')
def get_diff(img1, img2):
    image_1 = Image.open(img1).convert('RGB')
    image_2 = Image.open(img2).convert('RGB')
    diff = ImageChops.difference(image_1, image_2).getbbox()
    return diff


@allure.title('Главная страница. Страница поиска. В title есть "Инженер по тестированию".')
def test_main():
    browser = open_browser(url='https://samara.hh.ru')
    with allure.step('Ищем поле для ввода'):
        search_field = browser.find_element(By.NAME, 'text')
    with allure.step('Отправляем значение "Инженер по тестированию"'):
        search_field.send_keys('Инженер по тестированию')
    search_field.send_keys(Keys.RETURN)
    with allure.step('Проверяем значение в title'):
        assert 'Работа инженером по тестированию в Самаре' in browser.title


@allure.title('Поиск. Установка фильтров и переход на страницу отфильтрованных вакансий.')
def test_filters():
    browser = open_browser(url='https://samara.hh.ru/vacancies/inzhener_po_testirovaniyu')
    with allure.step('Ищем кнопку расширенного поиска'):
        filters_button = browser.find_element(By.CLASS_NAME, 'bloko-icon-link')
        with allure.step('Нажимаем на кнопку расширенного поиска'):
            filters_button.click()
    browser.implicitly_wait(3)

    with allure.step('Ищем кнопку удаления региона'):
        delete_region = browser.find_element(By.CLASS_NAME, 'bloko-tag-button')
        browser.execute_script("arguments[0].scrollIntoView();", delete_region)
        with allure.step('Нажимаем кноку удаления региона'):
            delete_region.click()

    with allure.step('Ищем поле зарплаты'):
        salary = browser.find_element(By.XPATH, salary_field)
        browser.execute_script("arguments[0].scrollIntoView();", salary)
        with allure.step('Указываем желаемую зарплату'):
            salary.send_keys('200000')

    with allure.step('Ищем чекбокс "Только с указанной зарплатой"'):
        only_with_salary = browser.find_element(By.XPATH, only_with_salary_field)
        browser.execute_script("arguments[0].scrollIntoView();", only_with_salary)
        with allure.step('Проставляем чекбокс "Только с указанной зарплатой'):
            only_with_salary.click()

    with allure.step('Ищем поле "Требуемый опыт работы: от 3 до 6 лет"'):
        experience = browser.find_element(By.XPATH, experience_field)
        browser.execute_script("arguments[0].scrollIntoView();", experience)
        with allure.step('Проставляем поле "Требуемый опыт работы: от 3 до 6 лет"'):
            experience.click()

    with allure.step('Ищем поле "Тип занятости: Полная занятость"'):
        type_of_work = browser.find_element(By.XPATH, type_field)
        browser.execute_script("arguments[0].scrollIntoView();", type_of_work)
        with allure.step('Проставляем поле "Тип занятости: Полная занятость"'):
            type_of_work.click()

    with allure.step('Ищем поле "График работы: Удалённая работа'):
        remote_work = browser.find_element(By.XPATH, remote_work_field)
        browser.execute_script("arguments[0].scrollIntoView();", remote_work)
        with allure.step('Проставляем поле "График работы: Удалённая работа"'):
            remote_work.click()

    with allure.step('Ищем кнопку "Найти"'):
        search_button = browser.find_element(By.XPATH, search_button_field)
        browser.execute_script("arguments[0].scrollIntoView();", search_button)
        with allure.step('Нажимаем кнопку "Найти"'):
            search_button.click()
            browser.implicitly_wait(3)
    total_vacancies = browser.find_element(By.TAG_NAME, 'h1').text
    with allure.step('Проверяем значение в title'):
        assert 'инженер по тестированию' in total_vacancies


@allure.title('Страница вакансии. Заполнение поля e-mail для отклика')
def test_open_result():
    browser = open_browser(url=open_result_url)
    browser.maximize_window()

    with allure.step('Ищем кнопку "Откликнуться"'):
        apply_button = browser.find_element(By.XPATH, apply_button_field)
        with allure.step('Нажимаем кнопку "Откликнуться"'):
            apply_button.click()
            sleep(3)
    with allure.step('Ищем поле для ввода e-mail'):
        apply_email = browser.find_element(By.NAME, 'login')
        with allure.step('Отправляем значение в поле e-mail'):
            apply_email.send_keys('balykov_ms@mail.ru')
    with allure.step('Кликаем мимо, чтобы пропал курсор в поле e-mail'):
        outside = browser.find_element(By.XPATH, outside_field)
        outside.click()
        sleep(1)
    with allure.step('Ищем весь блок отклика'):
        apply_whole = browser.find_element(By.XPATH, apply_whole_field)
        browser.execute_script("arguments[0].scrollIntoView();", apply_whole)
    with allure.step('Делаем скриншот для сравнения'):
        apply_whole.screenshot('filled_apply.png')
    with allure.step('Сравниваем скриншот с эталоном'):
        diff = get_diff(img1='reference.png', img2='filled_apply.png')
        allure.attach.file('C:\\Users\\che1o\\PycharmProjects\\vk_automation\\reference.png',
                           attachment_type=allure.attachment_type.PNG)
        allure.attach.file('C:\\Users\\che1o\\PycharmProjects\\vk_automation\\filled_apply.png',
                           attachment_type=allure.attachment_type.PNG)
    assert diff is None, "Images doesn't match"


"""To generate allure report we need:
* In terminal: pytest -v test.py --alluredir=/tmp/my_allure_results
* In PowerShell: allure serve /tmp/my_allure_results"
"""