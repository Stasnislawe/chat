import requests
from django.test import TestCase
from django.urls import reverse
from project.wsgi import *
from .models import Chat, Message, UserProfile
from django.contrib.auth.models import User


# python -m unittest chat.tests.ModelUsersTest / ViewTest
class ModelUsersTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user_test_1', email='1@mail.ru', password='Tea3sdZ31S5X-1')
        user2 = User.objects.create_user(username='user_test_2', email='2@mail.ru', password='Xre4sdN18T5X-9')
        user3 = User.objects.create_user(username='user_test_3', email='3@mail.ru', password='Xre4sdZ31S5X-1')
        self.object1 = UserProfile.objects.create(user=user1, name='test_userprofile_1')
        self.object2 = UserProfile.objects.create(user=user2, name='test_userprofile_2')
        self.object3 = UserProfile.objects.create(user=user3, name='test_userprofile_3')

    def test_str_representation(self):
        self.assertEqual(str(self.object1.name), 'test_userprofile_1')
        self.assertEqual(str(self.object2.name), 'test_userprofile_2')
        self.assertEqual(str(self.object3.name), 'test_userprofile_3')

    def tearDown(self):
        pass


class ViewTest(TestCase):
    def test_view_status_code(self):
        url_login = reverse('login')
        response_login = self.client.get(url_login)
        self.assertEqual(response_login.status_code, 200)
        url_signup = reverse('signup')
        response_signup = self.client.get(url_signup)
        self.assertEqual(response_signup.status_code, 200)
        """ Код 302, т.к переход на url_name 'dialogs' / 'users' возможен только 
        зарегестрированным пользователям => соответсвтенно код будет 302 """
        url_dialogs = reverse('dialogs')
        response_dialogs = self.client.get(url_dialogs)
        self.assertEqual(response_dialogs.status_code, 302)
        url_users = reverse('users')
        response_users = self.client.get(url_users)
        self.assertEqual(response_users.status_code, 302)


        # url2 = reverse('signup')
        # response2 = self.client.get(url2)
        # self.assertEqual(response2.status_code, 200)
        # url3 = reverse('logout')
        # response3 = self.client.get(url3)
        # self.assertEqual(response3.status_code, 200)

    # def test_view_template_used(self):
        # url1 = reverse('login')
        # response1 = self.client.get(url1)
        # self.assertTemplateUsed(response1, 'registration/login.html')
        # url2 = reverse('signup')
        # response2 = self.client.get(url2)
        # self.assertTemplateUsed(response2, 'registration/signup.html')
        # url3 = reverse('logout')
        # response3 = self.client.get(url3)
        # self.assertTemplateUsed(response3, 'registration/logout.html')