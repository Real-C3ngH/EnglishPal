import random
import string
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from helper import signup

def has_punctuation(s):
    return any(c in string.punctuation for c in s)

def select_one(driver):
    elem = driver.find_element(By.ID, 'article')
    essay_content = elem.text
    valid_word = random.choice([word for word in essay_content.split() if len(word) >= 6 and not has_punctuation(
        word) and 'font>' not in word and 'br>' not in word and 'p>' not in word])
    driver.find_element(By.ID, 'selected-words').send_keys(valid_word)
    driver.find_element(By.ID, 'article').click()
    return valid_word

def select_two(driver):
    word = driver.find_element(By.CLASS_NAME, 'highlighted')

    # 创建ActionChains对象
    actions = ActionChains(driver)
    actions.move_to_element(word)

    # 模拟鼠标按下并拖动以选择文本
    actions.double_click()
    actions.perform()


def test_selected_second_word(driver, URL):
    try:
        signup(URL, driver)
        selected_words = select_one(driver);
        assert selected_words.strip() != "", "选中的单词被放置框中"
        select_two(driver)
        selected_second_words = driver.find_element(By.ID, 'selected-words').get_attribute('value')
        assert selected_second_words.strip() == "", "选中的单词被删除"
    finally:
        driver.quit()
