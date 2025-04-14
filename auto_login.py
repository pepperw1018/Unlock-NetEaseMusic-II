# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D5C3D164B5ED4F1A4DCD00C7104EB5BB8A78F2850AFCE1378B72EE7EE1A34D215C7B7D0F91B493E510F0F0205A738F26CA8429F0720854CB9AD964C71B86817123B8E0BA38B9EF29AF1DAAA266474BF4293E5DF16526CEEB839221CEF392B1B4A375B2990D3CEFC3A95649827EBE740AE9250C7C9B823BCD0B405BA396EBC8EB59169F26C37AB799258643BEA4A7C2A2B417DE1C96F474D08466AD110D0D1EE03603D8ED38A4457E7B43F3B0C1AF5EF3BC32F77CA43AE3D5C146BA5F9937A291F381846848C5DA4B3FB012A33C0C1FE636DECA2D40ADBCC22A420EA94138ED548670C966BEEBA807222D8C910AE53A53197E91EA487C096AB2BCB2F9595E0EB17D167A04540EF09406C9CC7783C7A1DC745D2497190B6448E7FE30C6CE47D18A6BBD32D7B22765EE6F150D60FA18B6116A0F0479666DC39A77901171E0AC056F9ECE9778E6007FD313C42A469598673AB2254283B605685738B3E425B66870AD"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
