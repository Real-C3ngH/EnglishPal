from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from helper import signup

def login(driver, home, uname, password):
    driver.get(home)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, '登录'))).click()
    driver.find_element(By.ID, 'username').send_keys(uname)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.XPATH, '//button[text()="登录"]').click()
    WebDriverWait(driver, 10).until(EC.title_is(f"EnglishPal Study Room for {uname}"))

def logout(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, '退出'))).click()

# 标记文章
def collect_article(driver):
    driver.find_element(By.XPATH, '//button[text()="标记文章"]').click()

def test_collect_article(driver, URL):
    try:
        username, password = signup(URL, driver)
        title = driver.find_element(By.ID, 'article_title').text
        article = driver.find_element(By.ID, 'article').text

        collect_article(driver)
        collected_title = driver.execute_script('return localStorage.getItem("articleTitle");')
        assert title == collected_title, "Unable to add the article to your collection."

        # 退出登录
        logout(driver)

        # 再次登录并检查收藏状态
        login(driver, URL, username, password)
        rechecked_title = driver.execute_script('return localStorage.getItem("articleTitle");')
        assert title == rechecked_title, "Collected article not found after re-login."

    except Exception as e:
        # 输出异常信息
        logging.error(e)
    finally:
        driver.quit()