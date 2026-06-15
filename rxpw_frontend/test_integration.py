# coding:utf-8

import os
from pathlib import Path
from unittest import TestCase
from unittest import main
from unittest import mock
from urllib.parse import urljoin

from reflex.testing import AppHarness
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import \
    presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait

from reflex_xpw_settings import CONFIG

os.environ["APP_HARNESS_HEADLESS"] = "true"


class TestApp(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.harness = AppHarness.create(root=Path(__file__).parent.parent)
        cls.harness.start()

        assert (frontend_url := cls.harness.frontend_url) is not None
        cls.logout_url = urljoin(frontend_url, CONFIG.routes.logout)
        cls.login_url = urljoin(frontend_url, CONFIG.routes.login)
        cls.index_url = urljoin(frontend_url, "index")
        cls.frontend_url = frontend_url

        cls.options = Options()
        cls.options.add_argument("--no-sandbox")
        cls.options.add_argument("--disable-gpu")
        cls.options.add_argument("--headless=new")
        cls.options.add_argument("--disable-dev-shm-usage")
        cls.options.add_argument("--window-size=1920,1080")

        cls.save_dir = Path(__file__).parent / "screenshots"
        cls.save_dir.mkdir(parents=True, exist_ok=True)

        cls.username = "demo"
        cls.password = "test"

    @classmethod
    def tearDownClass(cls):
        cls.harness.stop()

    def setUp(self):
        self.driver = self.harness.frontend(
            driver_clz=webdriver.Chrome,
            driver_options=self.options,
        )
        self.assertIsInstance(self.driver, WebDriver)

    def tearDown(self):
        self.driver.quit()

    def save_screenshot(self, filename: str):
        self.assertTrue(self.driver.save_screenshot(self.save_dir / filename))

    def test_instance(self):
        self.assertIsNotNone(self.harness.app_instance)
        self.assertIsNotNone(self.harness.frontend_url)
        self.assertIsNotNone(self.harness.backend)

    def test_about_page(self):
        self.driver.get(urljoin(self.frontend_url, "about"))
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "text")))  # noqa:E501
        self.save_screenshot("about_page.png")

    def test_hello_page(self):
        self.driver.get(url := urljoin(self.frontend_url, "hello"))
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != url)
        self.assertEqual(self.driver.current_url, f"{self.login_url}?src=/hello")  # noqa:E501
        self.save_screenshot("hello_page_redirect_to_login.png")

    def test_index_page(self):
        self.driver.get(url := self.frontend_url)
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != url)
        self.assertEqual(self.driver.current_url, f"{self.login_url}?src=/")  # noqa:E501
        self.save_screenshot("index_page_redirect_to_login.png")

    def test_login_input_username_is_empty(self):
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "username"))).clear()  # noqa:E501
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "password"))).send_keys(self.password)  # noqa:E501
        self.save_screenshot("login_only_input_password.png")
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "submit"))).click()  # noqa:E501
        self.save_screenshot("login_prompt_username_is_empty.png")

    def test_login_input_password_is_empty(self):
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "username"))).send_keys(self.username)  # noqa:E501
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "password"))).clear()  # noqa:E501
        self.save_screenshot("login_only_input_username.png")
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "submit"))).click()  # noqa:E501
        self.save_screenshot("login_prompt_password_is_empty.png")

    def test_login_and_logout_click_button(self):
        self.driver.get(url := self.frontend_url)
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != url)
        self.assertEqual(self.driver.current_url, f"{self.login_url}?src=/")

        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.save_screenshot("login_input.png")
        self.driver.find_element(By.ID, "submit").click()

        WebDriverWait(self.driver, 10).until(lambda d: d.current_url == url)
        self.assertEqual(self.driver.current_url, url)
        self.save_screenshot("login_successful.png")

        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "logout"))).click()  # noqa:E501
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != url)
        self.assertEqual(self.driver.current_url, f"{self.login_url}?src=/")
        self.save_screenshot("login_page.png")

    def test_login_and_logout_url(self):
        self.driver.get(url := self.frontend_url)
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != url)
        self.assertEqual(self.driver.current_url, f"{self.login_url}?src=/")

        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "submit").click()

        WebDriverWait(self.driver, 10).until(lambda d: d.current_url == url)
        self.assertEqual(self.driver.current_url, url)

        self.driver.get(url := urljoin(self.frontend_url, "hello"))
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "text")))  # noqa:E501
        self.assertEqual(self.driver.current_url, url)
        self.save_screenshot("hello_page.png")

        self.driver.get(url := self.login_url)
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != url)
        self.assertEqual(self.driver.current_url, self.frontend_url)
        self.save_screenshot("index_page.png")

        self.driver.get(url := self.logout_url)
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != url)
        self.assertEqual(self.driver.current_url, f"{self.login_url}?src=/")

    @mock.patch.object(CONFIG.access, "logout", mock.MagicMock(return_value=False))  # noqa:E501
    def test_logout(self):
        self.driver.get(self.logout_url)
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "prompt")))  # noqa:E501
        self.assertEqual(self.driver.current_url, self.logout_url)
        self.save_screenshot("logout_page.png")

    @mock.patch.object(CONFIG.access, "logout", mock.MagicMock(return_value=False))  # noqa:E501
    def test_logout_error(self):
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "username"))).send_keys(self.username)  # noqa:E501
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "password"))).send_keys(self.password)  # noqa:E501
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "submit"))).click()  # noqa:E501
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != self.login_url)  # noqa:E501
        self.assertEqual(self.driver.current_url, self.frontend_url)
        self.save_screenshot("logout_error_logged_in.png")

        self.driver.get(self.logout_url)
        WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "prompt")))  # noqa:E501
        self.assertEqual(self.driver.current_url, self.logout_url)
        self.save_screenshot("logout_error_uable_to_log_out.png")


if __name__ == "__main__":
    main()
