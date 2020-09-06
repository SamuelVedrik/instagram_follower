from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from login import *
import pandas as pd
from tqdm.auto import tqdm


class FollowBot:

    def __init__(self):

        self.logged_in = False

        # Initiate driver
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self, username, password):
        """
        Logs into the given instagram account.
        """

        self.logged_in = True

        self.driver.get("https://instagram.com/accounts/login")
        self.driver.implicitly_wait(100)

        username_element = self.driver.find_element_by_css_selector(
            "input[name='username']")
        password_element = self.driver.find_element_by_css_selector(
            "input[name='password']")

        username_element.send_keys(username)
        password_element.send_keys(password, Keys.ENTER)

        try:
            not_now = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "div.cmbtv > button.sqdOP.yWX7d.y3zKF")))

            not_now.click()

        finally:
            pass

    def go_to_user(self, username):
        self.driver.get(f"https://instagram.com{username}")

    def get_followers(self, username):
        """
        Returns the followers of the user. If there are more than 999 followers,
        it may not return them all.

        The username must be given in the format of
        '/username'.

        Raises an exception if not logged in.
        """
        if not self.logged_in:
            raise NotLoggedInException

        self.go_to_user(username)
        self.driver.implicitly_wait(100)

        followers = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.-nal3"))
        )
        followers.click()

        dialog = self.driver.find_element_by_css_selector(".isgrP")

        try:
            limit = int(
                self.driver.find_element_by_xpath("//li[2]/a/span").text)
        except ValueError:
            limit = 500

        for _ in tqdm(range(limit)):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            time.sleep(0.2)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        return soup.select("a.FPmhX.notranslate._0imsa")

    def follow_user(self, username):
        """
        Follows the given user.
        The username must be given in the format of
        '/username'

        Raises an exception if not logged in.
        """
        if not self.logged_in:
            raise NotLoggedInException

        self.go_to_user(username)
        self.driver.implicitly_wait(0.3)
        try:

            follow = self.driver.find_element_by_css_selector(
                "button._5f5mN.jIbKX._6VtSN.yZn4P")

        except:

            follow = self.driver.find_element_by_css_selector(
                "button.sqdOP.L3NKy.y3zKF")

        follow.click()


class NotLoggedInException(Exception):

    def __repr__(self):
        return "Please login before executing other functions."


if __name__ == "__main__":

    bot = FollowBot()
    bot.login(USERNAME, PASSWORD)
    profiles = bot.get_followers("/nasa")
    profiles = [profile["href"] for profile in profiles]
    _ = [bot.follow_user(profile) for profile in profiles]
