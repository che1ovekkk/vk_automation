from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def test_main():
    browser = webdriver.Chrome()
    browser.get(url='https://samara.hh.ru')
    browser.implicitly_wait(3)
    elem = browser.find_element(By.NAME, 'text')
    elem.send_keys('Инженер по тестированию')
    elem.send_keys(Keys.RETURN)
    assert 'Работа инженером по тестированию в Самаре' in browser.title


def test_filters():
    browser = webdriver.Chrome()
    browser.get(url='https://samara.hh.ru/vacancies/inzhener_po_testirovaniyu')
    browser.implicitly_wait(3)
    filters_button = browser.find_element(By.CLASS_NAME, 'bloko-icon-link')
    filters_button.click()
    browser.implicitly_wait(3)
    delete_region = browser.find_element(By.CLASS_NAME, 'bloko-tag-button')
    browser.execute_script("arguments[0].scrollIntoView();", delete_region)
    delete_region.click()
    salary = browser.find_element(By.XPATH,
                                  '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div[1]/form/div[6]/div/div[2]/div[1]/div[1]/fieldset/input')
    browser.execute_script("arguments[0].scrollIntoView();", salary)
    salary.send_keys('200000')
    only_with_salary = browser.find_element(By.XPATH,
                                            '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div[1]/form/div[6]/div/div[2]/div[2]/label/span')
    browser.execute_script("arguments[0].scrollIntoView();", only_with_salary)
    only_with_salary.click()
    expirience = browser.find_element(By.XPATH,
                                      '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div[1]/form/div[7]/div/div[2]/div[4]/label/span')
    browser.execute_script("arguments[0].scrollIntoView();", expirience)
    expirience.click()
    type = browser.find_element(By.XPATH,
                                '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div[1]/form/div[8]/div/div[2]/div[1]/label/span')
    browser.execute_script("arguments[0].scrollIntoView();", type)
    type.click()
    remote_work = browser.find_element(By.XPATH,
                                       '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div[1]/form/div[9]/div/div[2]/div[4]/label/span')
    browser.execute_script("arguments[0].scrollIntoView();", remote_work)
    remote_work.click()
    search_button = browser.find_element(By.XPATH,
                                         '//*[@id="HH-React-Root"]/div/div[3]/div[1]/div/div/div[1]/form/div[15]/div[2]/button')
    browser.execute_script("arguments[0].scrollIntoView();", search_button)
    search_button.click()
    browser.implicitly_wait(3)
    total_vacancies = browser.find_element(By.TAG_NAME, 'h1').text
    assert 'инженер по тестированию' in total_vacancies
