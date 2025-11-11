import time
import pytest
import uuid
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, NoSuchElementException, \
    TimeoutException
from conftest import URL
driver = webdriver.Chrome()
def test_bug555():
    try:
        driver.maximize_window()
        base_url = "http://127.0.0.1:5000"
        driver.get(base_url)
        article = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'article')))
        perform_actions_on_article(driver, article)

        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'load_next_article')))
        next_button.click()
        print("Clicked next article button.")

        prev_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'load_pre_article')))
        prev_button.click()
        print("Clicked previous article button.")

    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
        print("Driver closed.")

def perform_actions_on_article(driver, article):
    actions = ActionChains(driver)
    actions.move_to_element(article)
    actions.click_and_hold()
    actions.move_by_offset(450, 200)
    actions.release()
    actions.perform()
    print("Performed actions on article.")