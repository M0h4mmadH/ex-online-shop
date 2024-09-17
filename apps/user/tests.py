from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User
from unittest.mock import patch


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.verify_otp_url = reverse('verify-otp')
        self.login_url = reverse('login')

    @patch('apps.user.services.generate_otp')
    def test_register_with_email(self, mock_generate_otp):
        mock_generate_otp.return_value = '123456'
        data = {
            'email': 'mikewazowski@minc.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP sent')

        # Verify OTP
        verify_data = {
            'login': 'mikewazowski@minc.com',
            'otp': '123456'
        }
        response = self.client.post(self.verify_otp_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.active.count(), 1)
        self.assertEqual(User.active.get().email, 'mikewazowski@minc.com')

    @patch('apps.user.services.generate_otp')
    def test_register_with_phone_number(self, mock_generate_otp):
        mock_generate_otp.return_value = '123456'
        data = {
            'phone_number': '09123456789',
            'password': 'testpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP sent')

        # Verify OTP
        verify_data = {
            'login': '09123456789',
            'otp': '123456'
        }
        response = self.client.post(self.verify_otp_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.active.count(), 1)
        self.assertEqual(User.active.get().phone_number, '09123456789')

    def test_login_with_email(self):
        user = User.objects.create_user(
            email='mikewazowski@minc.com',
            password='testpassword123'
        )
        data = {
            'login': 'mikewazowski@minc.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_phone_number(self):
        user = User.objects.create_user(
            phone_number='09123456789',
            password='testpassword123'
        )
        data = {
            'login': '09123456789',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials(self):
        data = {
            'login': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_without_email_or_phone_number(self):
        data = {
            'password': 'testpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('apps.user.services.generate_otp')
    def test_register_with_invalid_otp(self, mock_generate_otp):
        mock_generate_otp.return_value = '123456'
        data = {
            'email': 'mikewazowski@minc.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to verify with invalid OTP
        verify_data = {
            'login': 'mikewazowski@minc.com',
            'otp': '654321'
        }
        response = self.client.post(self.verify_otp_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.active.count(), 0)
