from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from organization.models import Organisation
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class TokenGenerationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            userId='testuser',
            firstName='Test',
            lastName='User',
            email='testuser@example.com',
            password='password123'
        )

    def test_token_contains_user_details(self):
        refresh = RefreshToken.for_user(self.user)
        decoded_token = refresh.access_token.payload

        self.assertEqual(str(decoded_token['user_id']), str(self.user.id))



class OrganisationAccessTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            userId='user1', firstName='John', lastName='Doe', email='john@example.com', password='password123'
        )
        self.user2 = User.objects.create_user(
            userId='user2', firstName='Jane', lastName='Smith', email='jane@example.com', password='password456'
        )

        self.org1 = Organisation.objects.create(name="John's Organisation")
        self.org2 = Organisation.objects.create(name="Jane's Organisation")

        self.org1.users.add(self.user1)
        self.org2.users.add(self.user2)

        self.client = APIClient()

    def test_user_access_own_organisation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/organisations/{self.org1.orgId}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_no_access_other_organisation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/organisations/{self.org2.orgId}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RegisterEndpointTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_success_default_org(self):
        """
        Test successful registration with default organization creation.
        """
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'userId': 'user123'
        }

        response = self.client.post('/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        user = User.objects.get(email=data['email'])
        self.assertIsNotNone(user)


        expected_org_name = f"{data['firstName']}'s Organisation"
        organization = Organisation.objects.get(name=expected_org_name)
        self.assertIsNotNone(organization)
        self.assertIn(user, organization.users.all())


        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['userId'], str(user.userId))
        self.assertEqual(response.data['data']['user']['firstName'], user.firstName)
        self.assertEqual(response.data['data']['user']['lastName'], user.lastName)
        self.assertEqual(response.data['data']['user']['email'], user.email)

    def test_login_success(self):
        """
        Test successful login with valid credentials.
        """

        data = {
            'firstName': 'Jane',
            'lastName': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password456',
            'userId': 'user456'
        }
        self.client.post('/auth/register/', data, format='json')


        login_data = {
            'email': 'jane.smith@example.com',
            'password': 'password456'
        }
        response = self.client.post('/auth/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], login_data['email'])

    def test_missing_required_fields(self):
        """
        Test registration with missing required fields.
        """

        test_cases = [
            {'lastName': 'Doe', 'email': 'john.doe@example.com', 'password': 'password123'},
            {'firstName': 'John', 'email': 'john.doe@example.com', 'password': 'password123'},
            {'firstName': 'John', 'lastName': 'Doe', 'password': 'password123'},
            {'firstName': 'John', 'lastName': 'Doe', 'email': 'john.doe@example.com'},
        ]

        for data in test_cases:
            response = self.client.post('/auth/register/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
            self.assertEqual(response.data['status'], 'Bad request')

    def test_duplicate_email(self):
        """
        Test registration with a duplicate email.
        """

        existing_user = User.objects.create_user(
            userId='testuser', firstName='Jane', lastName='Smith', email='jane.smith@example.com',
            password='password456'
        )

        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'jane.smith@example.com',  # Existing email
            'password': 'password123',
            'userId': 'user123'
        }

        response = self.client.post('/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


        self.assertIn('email', response.data['errors'])
