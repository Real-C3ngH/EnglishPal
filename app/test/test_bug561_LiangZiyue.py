import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_bug561_LiangZiyue(driver, URL):
    try:
        driver.get(home)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, '登录'))).click()
        driver.find_element(By.ID, 'username').send_keys("wrr")
        driver.find_element(By.ID, 'password').send_keys("1234")
        driver.find_element(By.XPATH, '//button[text()="登录"]').click()
        ele = driver.find_element(By.XPATH,'//font[@id="article"]')
        driver.execute_script('arguments[0].scrollIntoView();',ele)
        action = ActionChains(driver)
        action.click_and_hold(ele)
        action.move_by_offset(0,500)
        action.perform()
        next_ele = driver.find_element(By.ID,'//button[@id="load_next_article"]')
        driver.execute_script('arguments[0].scrollIntoView();',next_ele)
        next_ele.click()
        driver.execute_script('arguments[0].scrollIntoView();',ele)
        ele.click()
    finally:
        driver.quit()