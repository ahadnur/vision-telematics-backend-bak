from django.test import TestCase
from apps.accounts.models import UserRole, User
from apps.accounts.serializers import UserWriteSerializer


class UserTestCase(TestCase):
    def setUp(self):
        self.user_type_admin = UserRole.objects.create(name='admin')
        self.user_type_user = UserRole.objects.create(name='user')

        self.valid_data = {
            'email': 'test@example.com',
            'password': 'securepassword',
            'user_type': self.user_type_admin.id,
            'first_name': 'Mr',
            'last_name': 'Name'
        }

        self.invalid_data = {
            'email': 'test@example.com',
            # 'password': 'short',
            'user_type': self.user_type_admin,
            'first_name': 'Mr',
            'last_name': 'Name'
        }

        self.existing_user = User.objects.create_user(
            email='existing@example.com',
            password='securepassword',
            user_type=self.user_type_admin,
            first_name='Mr',
            last_name='Nas'
        )

    def test_user_unique_email(self):
        pass
    def test_user_serializer_valid_data(self):
        serializer = UserWriteSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")
        user = serializer.save()
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertTrue(user.check_password(self.valid_data['password']))
        self.assertEqual(user.user_type.id, self.valid_data['user_type'])

    def test_user_serializer_invalid_password(self):
        serializer = UserWriteSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
