import time
from django.test import TestCase

from project.wsgi import *
from django.test import Client
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
        cls.options = webdriver.FirefoxOptions()
        cls.options.add_argument("--headless")
        cls.selenium = webdriver.Firefox(service=cls.service, options=cls.options)

    """Регистрация с последующей авторизацией через селениум"""
    def test_login(self):
        # Задаем юрл
        self.selenium.get(f'{self.live_server_url}/accounts/signup/')
        username = 'Test1'
        mail = '1@mail.ru'
        password = 's4Dsa612H_21Zr'
        # Селениум ищет и заполняет поля регистрации
        username_input = self.selenium.find_element("xpath", "//input[@id='id_username']")
        username_input.send_keys(username)
        email_input = self.selenium.find_element("xpath", "//input[@id='id_email']")
        email_input.send_keys(mail)
        password1 = self.selenium.find_element("xpath", "//input[@id='id_password1']")
        password1.send_keys(password)
        password2 = self.selenium.find_element("xpath", "//input[@id='id_password2']")
        password2.send_keys(password)
        # Поиск кнопки "регистрация"
        registration_button = self.selenium.find_element("xpath", "//button[@id='regbutton']")
        registration_button.click()
        # Небольшая пауза для корректной работы
        time.sleep(1)
        # Авторизация по данным зарегестрированным секунду назад
        login_username = self.selenium.find_element("xpath", "//input[@id='id_username']")
        login_username.send_keys(username)
        login_password = self.selenium.find_element("xpath", "//input[@id='id_password']")
        login_password.send_keys(mail)
        login_button = self.selenium.find_element("xpath", "//button[@id='logbutton']")
        login_button.click()

        # Проверка что пользователь создан
        self.object = User.objects.get(username=username)
        self.assertEqual(str(self.object.username), username)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class LoginStatusCodeTest(TestCase):
    def setUp(self):
        self.username = 'user_test_1'
        self.password = 'Tea3sdZ31S5X-1'
        user = User.objects.create_user(username=self.username, email='1@mail.ru', password=self.password)

    def test_status_code_logined(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response_dialogs = c.get(reverse('dialogs'))
        self.assertEqual(response_dialogs.status_code, 200)
        response_users = c.get(reverse('users'))
        self.assertEqual(response_users.status_code, 200)

    def tearDown(self):
        pass