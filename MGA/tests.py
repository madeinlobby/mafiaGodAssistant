from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

# class UserModelTests(TestCase):
#
#     def create_user(self):
#         factory = APIRequestFactory()
#         request = factory.post('/signup/', {'username': 'zahra', 'password': 'zahra12345'})
#         self.assertIs(request, False)
from MGA.models import User


class UserAPITests(APITestCase):
    # def test_create_account(self):
    #     """
    #     Ensure we can create a new account object.
    #     """
    #     url = reverse('create')
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)

    def test_login_user(self):
        """
        Ensure login is ok!
        """
        url = reverse('login')
        data = {'username': 'saba', 'password': 'saba12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'DabApps')

    def test_create_user(self):
        """
             Ensure signup is ok!
        """
        url = reverse('signup')
        data = {'username': 'ctest', 'name': 'name', 'password': 'ctest12345', 'bio': 'bio',
                'phoneNumber': '9382593895', 'city': 'tehran', 'email': 'z.y.j.1379@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
