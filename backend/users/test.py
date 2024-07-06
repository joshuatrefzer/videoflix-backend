from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.core import mail
from rest_framework import status
from .models import CustomUser
from rest_framework.authtoken.models import Token


class RegisterViewTests(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_register_success(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('success', response.data)
        self.assertIn('Registration successful', response.data['success'])

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate Your Account')
        self.assertIn('testuser@example.com', mail.outbox[0].to)

    def test_register_invalid_data(self):
        url = reverse('register')
        data = {} 

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)  
        self.assertIn('password', response.data)

    def test_register_email_failure(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
        }

        with self.assertRaises(Exception):
            with self.settings(EMAIL_BACKEND='django.core.mail.backends.dummy.EmailBackend'):
                self.client.post(url, data, format='json')
                
                
                
class ActivateAccountViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            confirmation_token='valid_token'
        )

    def test_activate_account(self):
        url = reverse('activate_account', args=['valid_token'])

        response = self.client.get(url)

        self.user.refresh_from_db()

        self.assertTrue(self.user.is_activated)
        self.assertIsNone(self.user.confirmation_token)

        self.assertRedirects(response, '/success/', fetch_redirect_response=False)
        
        
        
class LoginViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            is_activated=True
        )

    def test_login_success(self):
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

        token = response.data['token']
        self.assertTrue(Token.objects.filter(key=token).exists())

    def test_login_invalid_password(self):
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid password', response.data['detail'])

    def test_login_inactive_account(self):
        self.user.is_activated = False
        self.user.save()

        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Your account is not activated', response.data['detail'])

    def test_login_user_not_found(self):
        url = reverse('login')
        data = {
            'email': 'nonexistentuser@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User not found', response.data['detail'])
        
        
        
class LogoutViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)

    def test_logout_success(self):
        url = reverse('logout')
        headers = {'Authorization': f'Token {self.token.key}'}

        response = self.client.post(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Logged out successfully', response.data['detail'])

        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_logout_invalid_token(self):
        url = reverse('logout')
        headers = {'Authorization': 'Token invalidtoken'}

        response = self.client.post(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid token', response.data['detail'])
        
        
        
        
class DeleteUserViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)

    def test_delete_user_success(self):
        url = reverse('delete_user')
        headers = {'Authorization': f'Token {self.token.key}'}

        response = self.client.post(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('User deleted successfully', response.data['detail'])

        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())

        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_delete_user_invalid_token(self):
        url = reverse('delete_user')
        headers = {'Authorization': 'Token invalidtoken'}

        response = self.client.post(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid token', response.data['detail'])

    def test_delete_user_user_not_found(self):
        self.user.delete()

        url = reverse('delete_user')
        headers = {'Authorization': f'Token {self.token.key}'}

        response = self.client.post(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User not found', response.data['detail'])
