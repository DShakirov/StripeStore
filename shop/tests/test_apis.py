from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from shop.models import Item


class CreateOrderTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.item, created = Item.objects.get_or_create(
            name='test_item',
            defaults={
                "description": "test item description",
                "price": 100500
            }
        )
    def test_success(self):
        payload = {
            'items': [{'id': self.item.id, 'name': self.item.name, 'price': self.item.price}, {'id': self.item.id, 'name': self.item.name, 'price': self.item.price},
                       {'id': self.item.id, 'name': self.item.name, 'price': self.item.price}]
        }

        response = self.client.post(
            reverse('create_order'), payload, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ItemListViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_success(self):
        response = self.client.get(
            reverse('items')
        )
        self.assertEqual(len(response.data), len(Item.objects.all()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PaymentIntentTestAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.item, created = Item.objects.get_or_create(
            name='test_item',
            defaults={
                "description": "test item description",
                "price": 100500
            }
        )

    def success(self):
        payload = {
            'items': [{'id': self.item.id, 'name': self.item.name, 'price': self.item.price}, {'id': self.item.id, 'name': self.item.name, 'price': self.item.price},
                       {'id': self.item.id, 'name': self.item.name, 'price': self.item.price}]
        }
        response = self.client.post(
            reverse('api/checkout'), payload, format='json'
        )
        self.assertEqual(len(response.data['clientSecret'] > 0, True))


