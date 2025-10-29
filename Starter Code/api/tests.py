from django.test import TestCase
from api.models import Order, User
from rest_framework import status
from django.urls import reverse
# Create your tests here.


class UserOrderTestCase(TestCase):
    """
    TestCase — Djangos test class that provides an isolated test database and helper methods.
    """

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)
        #setUp() is automatically executed before each test method in the class.
        #It prepares test data in a fresh test database.
        #Because TestCase uses a transactional test DB, these records exist only for the duration of the test and won’t affect your real database.

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(
            self):
        #Django’s test runner will detect and run it.
        user = User.objects.get(username='user1')
        #User.objects.get(...) fetches the user1 object we created in setUp.
        self.client.force_login(user)
        #self.client is Django’s test client. force_login(user) logs in the user for the test client without requiring a password.
        response = self.client.get(reverse('user-orders'))
        #reverse('user-orders') resolves the URL name 'user-orders' to the actual path (e.g. /api/orders/).

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order['user'] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
