from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Item, Order, OrderItem, Discount, Tax
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import stripe
from shop_app.settings import STRIPE_KEY
from .serializers import ItemSerializer, OrderSerializer


class BuyItemView(APIView):
    """
    Представление для покупки одного товара
    Получает с фронтенда id товара и создает Stripe Checkout Session
    """
    def get(self, request, id):
        print('works')
        item = Item.objects.get(id=id)
        stripe.api_key = STRIPE_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://127.0.0.1/success',
            cancel_url='https://127.0.0.1/cancel',
        )
        return Response({'session_id': session.id}, status=status.HTTP_200_OK)


class ItemView(DetailView):
    """
    Представление для отображение на фронтенде одиночного товара
    """
    model = Item
    template_name = 'index.html'


class SuccessView(View):
    """
    Представления для отображения шаблона об успешной покупке
    """
    def get(self, request, *args, **kwargs):
        return render(request, "success.html")


class CancelView(View):
    """
    Представления для отображения шаблона о неудачной покупке
    """
    def get(self, request, *args, **kwargs):
        return render(request, "cancel.html")


class ItemChoiceView(View):
    """
    Представление для отображения шаблона main.html
    """
    def get(self, request):
        return render(request, 'main.html')


class PremiumItemChoiceView(View):
    """
    Представление для отображения шаблона premium.html
    """
    def get(self, request):
        return render(request, 'premium.html')


class ItemsListView(generics.ListAPIView):
    """
    Представление для отображения списка продаваемых товаров
    """
    serializer_class = ItemSerializer
    queryset = Item.objects.filter(currency__name='USD')


class PremiumItemsListView(generics.ListAPIView):
    """
    Представление для отображения списка продаваемых за INR товаров
    """
    serializer_class = ItemSerializer
    queryset = Item.objects.filter(currency__name='INR')


class PaymentIntentAPIView(APIView):
    """
    Представление для получения покупки с фронтенда и создания Stripe Payment Intent
    """

    def post(self,request):
        # creating order
        new_order = Order.objects.create()
        total_price = 0
        name = []
        for cart_item in request.data['cart']:
            item = Item.objects.get(id=cart_item['id'])
            order_item = OrderItem.objects.create(
                order=new_order, item=item, price=cart_item['price']
            )
            total_price += item.price
            name.append(item.name)
        new_order.name = ', '.join(name)
        new_order.total_price = total_price
        new_order.save()
        # создание платежного интента
        stripe.api_key = STRIPE_KEY
        discounts = Discount.objects.filter(order=new_order)
        taxes = Tax.objects.filter(order=new_order)
        payment_intent_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': new_order.name,
                },
                'unit_amount': int(new_order.total_price * 100),
            },
            'quantity': 1,
        }]
        for discount in discounts:
            payment_intent_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Discount',
                    },
                    'unit_amount': int(-discount.amount * 100),
                },
                'quantity': 1,
            })
        for tax in taxes:
            payment_intent_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Tax',
                    },
                    'unit_amount': int(tax.amount * 100),
                },
                'quantity': 1,
            })

        payment_intent = stripe.PaymentIntent.create(
            amount=int(new_order.total_price * 100),
            currency='usd',
            payment_method_types=['card'],
            description='Payment for order: {}'.format(new_order.id),
            statement_descriptor='Custom descriptor',
            metadata={'order_id': new_order.id},
        )
        return Response({'clientSecret': payment_intent.client_secret}, status=status.HTTP_200_OK)


class PremiumPaymentIntentAPIView(APIView):
    """
    Представление для получения покупки с фронтенда и создания Stripe Payment Intent
    Действует для покупки за рупии
    """

    def post(self,request):
        # creating order
        new_order = Order.objects.create()
        total_price = 0
        name = []
        for cart_item in request.data['cart']:
            item = Item.objects.get(id=cart_item['id'])
            order_item = OrderItem.objects.create(
                order=new_order, item=item, price=cart_item['price']
            )
            total_price += item.price
            name.append(item.name)
        new_order.name = ', '.join(name)
        new_order.total_price = total_price
        new_order.save()
        # создание платежного интента
        stripe.api_key = STRIPE_KEY
        discounts = Discount.objects.filter(order=new_order)
        taxes = Tax.objects.filter(order=new_order)
        payment_intent_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': new_order.name,
                },
                'unit_amount': int(new_order.total_price * 100),
            },
            'quantity': 1,
        }]
        for discount in discounts:
            payment_intent_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Discount',
                    },
                    'unit_amount': int(-discount.amount * 100),
                },
                'quantity': 1,
            })
        for tax in taxes:
            payment_intent_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Tax',
                    },
                    'unit_amount': int(tax.amount * 100),
                },
                'quantity': 1,
            })

        payment_intent = stripe.PaymentIntent.create(
            amount=int(new_order.total_price * 100),
            currency='inr',
            payment_method_types=['card'],
            description='Payment for order: {}'.format(new_order.id),
            statement_descriptor='Custom descriptor',
            metadata={'order_id': new_order.id},
        )
        return Response({'clientSecret': payment_intent.client_secret}, status=status.HTTP_200_OK)