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
    browser.add_cookie({"name": "MUSIC_U", "value": "000EB0F4AADB84F0C7AB34E76041477007AFEDBE06B9884A58C18D4A51582B14892158DA49A2D226B4FCED2FBB89A572DE5EE528ADDC650DADD65A31E44B70574CD5DAD981148A94B99E4F275D32C067F0EDBDD3F7EF5A2D5146BCC6AB1FFFA0558BA67E0CDA72E3304CACF9F5AE0F3072AA2A26D7823218CB034EC6391DA1ECDFCA400D5C7DE13CCCDEF4172901A324B41E7C7987912538E8B1485556792933160905AE5375C9B01749E3AB8507C0B154C6BA50D0AAD6E0ECD87772CBF33F99F41A9E921E59AD6597CBCFD035A9B9EC9515172D8520EA2B108A6019F4D09E98975E69EE53D3E6D6035F24A690B67B9D3642E5DCD2C05AF037281F125653E41DDD45916EC3355F6BBB7772EA6475441ABFFDBBB0E557497BE7AF9D2D436E9B701AEB1DF5E5D010EBBB8B35B5C4A921642706F749C70B761E230E4A0444DEC6D1A364FE683235A408D205B9FCA564D182A19487A319CC0AC960FA0FB1204A19506A"})
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
