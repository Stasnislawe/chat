import requests
from django.test import TestCase, Client
from django.urls import reverse
from project.wsgi import *
from .models import Chat, Message, UserProfile
from django.contrib.auth.models import User


# python -m unittest chat.tests.ModelUsersTest / ViewTest / ChatTest

"""Создание моделей пользователя"""
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


class ChatTest(TestCase):
    """Создание диалога между двумя пользователями"""
    def setUp(self):
        self.object1 = User.objects.create_user(username='user_test_1', email='1@mail.ru', password='Tea3sdZ31S5X-1')
        self.object2 = User.objects.create_user(username='user_test_2', email='2@mail.ru', password='Xre4sdN18T5X-9')
        chat_model = Chat.objects.create()
        chat_model.members.add(self.object1)
        chat_model.members.add(self.object2)
        self.message = Message.objects.create(chat=chat_model, author=self.object1, message='Привет', is_readed=True)
        self.message2 = Message.objects.create(chat=chat_model, author=self.object2, message='Салют', is_readed=False)

    def test_messages(self):
        # Проверка сообщений
        self.assertEqual(str(self.message.message), 'Привет')
        self.assertEqual(str(self.message2.message), 'Салют')

    def test_is_readed(self):
        # Проверка что сообщения не прочитаны/прочитаны
        self.assertEqual(self.message2.is_readed, False)
        self.assertEqual(self.message.is_readed, True)

    def test_authors(self):
        # Проверка авторов сообщений
        self.assertEqual(self.message.author, self.object1)
        self.assertEqual(self.message2.author, self.object2)

    def tearDown(self):
        pass


class ViewTest(TestCase):
    """ Проверка вьюх с LoginRequiredMixin/login_required()
        Вывод response status_code должен быть 302"""
    def setUp(self):
        url_login = reverse('login')
        self.response_login = self.client.get(url_login)
        url_signup = reverse('signup')
        self.response_signup = self.client.get(url_signup)
        url_dialogs = reverse('dialogs')
        self.response_dialogs = self.client.get(url_dialogs)
        url_users = reverse('users')
        self.response_users = self.client.get(url_users)

    def test_view_login_status_code(self):
        self.assertEqual(self.response_login.status_code, 200)

    def test_view_signup_status_code(self):
        self.assertEqual(self.response_signup.status_code, 200)

    def test_view_dialogs_302_status_code(self):
        """ Код 302, т.к переход на url_name 'dialogs' / возможен только
        зарегестрированным пользователям => соответсвтенно код будет 302 """
        self.assertEqual(self.response_dialogs.status_code, 302)

    def test_view_users_302_status_code(self):
        """ Код 302, т.к переход на url_name 'users' возможен только
        зарегестрированным пользователям => соответсвтенно код будет 302 """
        self.assertEqual(self.response_users.status_code, 302)

    def tearDown(self):
        pass
