from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 对用户名不能为中文进行测试
def test_register_username_with_chinese(driver, URL):
    try:
        driver.get(URL + "/signup")

        # 等待用户名输入框出现
        username_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        username_elem.send_keys("测试用户")  # 输入中文用户名

        # 等待密码输入框出现
        password_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        password_elem.send_keys("validPassword123")  # 输入有效密码

        # 等待确认密码输入框出现
        password2_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password2'))
        )
        password2_elem.send_keys("validPassword123")  # 输入有效确认密码

        # 等待注册按钮出现并点击
        signup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@onclick="signup()"]'))
        )
        signup_button.click()

        # 等待警告框出现并接受
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"警告文本: {alert_text}")
        assert alert_text == "Chinese characters are not allowed in the user name."  # 根据实际的警告文本进行断言
        alert.accept()

    except Exception as e:
        print(f"发生错误: {e}")
        raise


# 对注册时密码不能是中文进行测试
def test_register_password_with_chinese(driver, URL):
    try:
        driver.get(URL + "/signup")

        # 等待用户名输入框出现
        username_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        username_elem.send_keys("validUsername123")  # 输入有效用户名

        # 等待密码输入框出现
        password_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        password_elem.send_keys("测试密码")  # 输入中文密码

        # 等待确认密码输入框出现
        password2_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password2'))
        )
        password2_elem.send_keys("测试密码")  # 输入中文确认密码

        # 等待注册按钮出现并点击
        signup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@onclick="signup()"]'))
        )
        signup_button.click()

        # 等待警告框出现并接受
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"警告文本: {alert_text}")
        assert alert_text == "Chinese characters are not allowed in the password."  # 根据实际的警告文本进行断言
        alert.accept()

    except Exception as e:
        print(f"发生错误: {e}")
        raise
