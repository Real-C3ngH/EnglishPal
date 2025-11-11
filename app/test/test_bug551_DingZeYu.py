import time
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helper import signup

def test_bug551(driver, URL):
    driver.maximize_window()
    driver.get(URL)

    username, password = signup(URL, driver)

    article = driver.find_element(By.ID, 'article')
    actions = ActionChains(driver)

    actions.move_to_element(article)
    actions.click_and_hold()
    actions.move_by_offset(450, 200)
    actions.release()
    actions.perform()

    # 获取选中高亮部分的单词的元素
    highlighted_words = driver.find_elements(By.CLASS_NAME, 'highlighted')

    # 验证选中部分的单词是否同时应用了需求样式
    expected_font_weight = "400"  

    for word in highlighted_words:
        font_weight = word.value_of_css_property("font-weight")
        assert font_weight == expected_font_weight, f"选中部分的单词的字体样式错误"

    time.sleep(5)
    driver.quit()
