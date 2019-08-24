from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase


class UserAPITests(APITestCase):
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
                'phoneNumber': '9382593895', 'city': 'tehran', 'email': 'z.y.j.1379@gmail.com'}
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
