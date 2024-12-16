import time

from project.wsgi import *
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


#  python -m unittest sign.tests.MySeleniumTests
class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.service = Service(executable_path=GeckoDriverManager().install())
        # cls.options = webdriver.FirefoxOptions()
        # cls.options.add_argument("--headless")
        cls.selenium = webdriver.Firefox(service=cls.service)

    def test_login(self):
        self.selenium.get(f'{self.live_server_url}/accounts/signup/')
        username_input = self.selenium.find_element("xpath", "//input[@id='id_username']")
        username_input.send_keys('Test1')
        email_input = self.selenium.find_element("xpath", "//input[@id='id_email']")
        email_input.send_keys('1@mail.ru')
        password1 = self.selenium.find_element("xpath", "//input[@id='id_password1']")
        password1.send_keys('s4Dsa612H_21Zr')
        password2 = self.selenium.find_element("xpath", "//input[@id='id_password2']")
        password2.send_keys('s4Dsa612H_21Zr')
        registration_button = self.selenium.find_element("xpath", "//button[@id='regbutton']")
        registration_button.click()
        time.sleep(2)
        login_username = self.selenium.find_element("xpath", "//input[@id='id_username']")
        login_username.send_keys('Test1')
        login_password = self.selenium.find_element("xpath", "//input[@id='id_password']")
        login_password.send_keys('s4Dsa612H_21Zr')
        login_button = self.selenium.find_element("xpath", "//button[@id='logbutton']")
        login_button.click()

        self.object = User.objects.get(username='Test1')
        self.assertEqual(str(self.object.username), 'Test1')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

