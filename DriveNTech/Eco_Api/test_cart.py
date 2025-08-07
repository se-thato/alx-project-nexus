from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Cart

class CartViewSetTests(APITestCase):
    def setUp(self):
        User = get_user_model()

        self.Thato = User.objects.create_user(username='Thato', password='password123')
        self.Xolani = User.objects.create_user(username='Xolani', password='password123')

        self.Thato_cart = Cart.objects.create(user=self.Thato)
        self.Xolani_cart = Cart.objects.create(user=self.Xolani)

        self.client.login(username='Thato', password='password123')

    def test_user_can_only_see_their_own_cart(self):
        response = self.client.get(reverse('cart-list')) 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['user'], self.Thato.id)
