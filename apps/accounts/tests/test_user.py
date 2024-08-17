from django.test import TestCase
from apps.accounts.models import UserRole, User
from apps.accounts.api.v1.serializers import UserWriteSerializer


class UserTestCase(TestCase):
    def setUp(self):
        self.role1 = UserRole.objects.create(name='admin')
        self.role2 = UserRole.objects.create(name='user')

        self.valid_data = {
            'email': 'test@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'role': [self.role1.id, self.role2.id],
        }

        self.invalid_data = {
            'email': 'test@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword2',
            'role': [self.role1.id, self.role2.id],
        }

        self.existing_user = User.objects.create_user(
            email='existing@example.com',
            password='securepassword',
        )

    def test_user_serializer_valid_data(self):
        serializer = UserWriteSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.check_password(self.valid_data['password1']))
        self.assertEqual(list(user.roles.values_list('id', flat=True)), [self.role1.id, self.role2.id])

    def test_user_serializer_invalid_password(self):
        serializer = UserWriteSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('no_fields_error', serializer.errors)