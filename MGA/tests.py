from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from MGA.models import User
from mafiaGodAssistant import settings


class Tests(APITestCase):
    def test_login_user(self):
        """
        Ensure login is ok!
        """
        self.test_create_user()  # make ctest in default db
        url = reverse('login')
        data = {'username': "ctest", 'password': "ctest12345"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Ensure signup is ok!
        """
        url = reverse('signup')
        data = {'username': 'ctest', 'name': 'name', 'password': 'ctest12345', 'bio': 'bio',
                'phoneNumber': '9382593895', 'city': 'tehran', 'email': 'z.y.j.1379@gmail.com', 'device': 'android'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logout_user(self):
        """
        Ensure logout is ok!
        """
        self.test_login_user()
        url = reverse('logout')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        """
        Ensure changing password is ok!
        """
        self.test_login_user()
        url = reverse('change_password')
        data = {'oldPassword': "ctest12345", 'newPassword': 'test12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        """
        Ensure reset password is ok!
        """
        self.test_create_user()
        url = reverse('reset_password')
        data = {'id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_friend(self):
        """
        Ensure friend request is ok!
        """
        self.test_login_user()
        self.test_create_user('b')
        url = reverse('MGA:send_friend_request')
        data = {'id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_friend(self):
        """
        Ensure friend request is ok!
        """
        self.test_request_friend()
        url = reverse('MGA:accept_friend_request')
        data = {'id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization(self):
        """
        Ensure create org is ok!
        """
        self.test_login_user()
        url = reverse('MGA:create_organization')
        data = {'name': "event"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_admin(self):
        """
        Ensure add admin is ok!
        """
        self.test_create_user()
        self.test_create_organization()
        url = reverse('MGA:add_admin')
        data = {'admin id': 1, 'org_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_event(self):
        """
        Ensure create event is ok!
        """
        self.test_create_organization()
        url = reverse('MGA:add_event')
        data = {'org_id': 1, 'title': 'first', 'capacity': 5, 'description': 'nothing!', 'date': now()}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_cafe(self):
        url = reverse('MGA:create_cafe')
        data = {'name': 'cafe', 'phoneNumber': '123456', 'telephone': '1234', 'capacity': 34, 'description': 'asdf',
                'forbiddens': "nothing!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_message(self):
        url = reverse('signup')
        data = {'username': 'mut', 'name': 'nme', 'password': 'ctest12345', 'bio': 'bio',
                'phoneNumber': '9382593895', 'city': 'tehran', 'email': 'z.j.1379@gmail.com', 'device': 'android'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_login_user()
        url = reverse('chat:send_to_one')
        data = {'text': 'hello', 'receiver_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_group(self):
        self.test_login_user()
        url = reverse('chat:create_group')
        data = {'name': 'gruop'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_message_to_group(self):
        self.test_create_group()
        url = reverse('chat:send_to_group')
        data = {'group_id': 1, 'text': 'hello'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_group(self):
        self.test_create_group()
        url = reverse('chat:delete_group', args=[1])
        data = {'id': 1}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_message(self):
        self.test_create_message()
        url = reverse('chat:edit_message')
        data = {'message_id': 1,'new_text':'hello'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message(self):
        self.test_edit_message()
        url = reverse('chat:get_message',args=[1])
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
