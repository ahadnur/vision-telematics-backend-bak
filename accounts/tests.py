from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTests(TestCase):

    def setUp(self):
        self.email = "amin@yopmail.com"
        self.password = 'nassifat'
        self.User = get_user_model()

    def test_create_user_with_email_password(self):
        user = self.User.cre
