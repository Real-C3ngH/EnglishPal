from selenium.webdriver.common.action_chains import ActionChains
from helper import signup


def test_highlight(driver, URL):
    try:
        # 打开网页
        driver.get(URL)
        driver.maximize_window()

        # 注册
        signup(URL, driver)

        # 取消勾选“划词入库按钮”
        highlight_checkbox = driver.find_element_by_id("chooseCheckbox")
        driver.execute_script("arguments[0].click();", highlight_checkbox)

        article = driver.find_element_by_id("article")

        # 创建 ActionChains 对象
        actions = ActionChains(driver)

        # 移动鼠标到起点位置
        actions.move_to_element(article)
        # actions.move_to_element_with_offset(article, 50, 100)
        # 按下鼠标左键
        actions.click_and_hold()
        # 拖动鼠标到结束位置
        actions.move_by_offset(400,50)
        # 释放鼠标左键
        actions.release()
        # 执行操作链
        actions.perform()
        # time.sleep(10)

        assert driver.find_elements_by_class_name("highlighted") is not None
    finally:
        # 测试结束后关闭浏览器
        driver.quit()