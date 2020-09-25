# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time


def fetch_tasks_info(config):
    username, password = config['username'], config['password']
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.set_window_size(1440, 3040)
        driver.get(
            'https://market.m.taobao.com/app/forest/assets/comeon.html?gameId=1')
        time.sleep(0.5)
        driver.switch_to.frame(0)
        driver.find_element_by_id('fm-login-id').send_keys(username)
        driver.find_element_by_id('fm-login-password').send_keys(password)

        time.sleep(1)
        try:
            ele_slider = driver.find_element_by_id('nc_1_n1z')
            ele_slider_container = driver.find_element_by_id('nc_1_n1t')
            ActionChains(driver).click_and_hold(
                on_element=ele_slider).perform()
            ActionChains(driver).move_by_offset(xoffset=(
                ele_slider_container.size['width'] - ele_slider.size['width']), yoffset=0).perform()
            ActionChains(driver).pause(0.5).release().perform()
        except NoSuchElementException:
            pass

        time.sleep(0.5)

        ele_submit = driver.find_element_by_css_selector(
            '#login-form > div.fm-btn > button')
        ele_submit.click()

        time.sleep(2)

        tasks = []
        ele_tasks = driver.find_element_by_xpath(
            "//div[starts-with(@class, 'tasks___')]")
        ele_task_items = ele_tasks.find_elements_by_xpath(
            ".//div[starts-with(@class, 'task_item___')]")

        finished_all = True
        for ele_task_item in ele_task_items:
            ele_task_content = ele_task_item.find_element_by_xpath(
                ".//span[starts-with(@class, 'content___')]")
            finished = "已完成" in ele_task_item.text
            if not finished:
                finished_all = False
            tasks.append(
                {'content': ele_task_content.text, 'finished': finished})

        days_of_checkin = ele_tasks.find_element_by_xpath(
            ".//div[starts-with(@class, 'content___')]").text
        schedule = ele_tasks.find_element_by_xpath(
            ".//div[starts-with(@class, 'schedule___')]").text

        return finished_all, days_of_checkin, schedule, tasks, ele_tasks.screenshot_as_png
    return None, None, None, None, None
