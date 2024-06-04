from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "password": "Azerty12345*",
            "birth_date": "2000-01-01",
            "can_be_contacted": True,
            "can_data_be_shared": False,
        }

    def test_create_user(self):
        response = self.client.post(reverse("register"), self.user_data, format="json")
        print(response.data)  # Ajoutez cette ligne pour inspecter la réponse
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_underage(self):
        self.user_data["birth_date"] = str(
            date.today().replace(year=date.today().year - 14)
        )
        response = self.client.post(reverse("register"), self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
