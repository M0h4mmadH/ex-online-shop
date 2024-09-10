from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.user.models import User
from .models import ProductCategory, Product, Cart, CartItem, PurchaseReceipt, Order, ReceiptOrder


class ShopAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin@test.com', 'adminpass')
        self.regular_user = User.objects.create_user('user@test.com', 'userpass')
        self.category = ProductCategory.objects.create(name='Electronics')
        self.product = Product.objects.create(name='Laptop', description='A good laptop', price=1000,
                                              category=self.category)

        Cart.objects.create(user=self.regular_user, cart_status='O')
        self.order = Order.objects.create(product=self.product, user=self.regular_user, price=95)
        self.receipt = PurchaseReceipt.objects.create(user=self.regular_user, price=95)
        ReceiptOrder.objects.create(order=self.order, user=self.regular_user, receipt=self.receipt)


    def test_admin_create_product(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin create products')
        data = {
            'name': 'New Product',
            'description': 'A new product description',
            'price': 99,
            'category': 'Electronics',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_admin_update_product(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin update products')
        data = {
            'id': self.product.id,
            'name': 'Updated Laptop',
            'price': 1200
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Laptop')
        self.assertEqual(self.product.price, 1200)

    def test_admin_create_category(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin create categories')
        data = {
            'name': 'Books',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductCategory.objects.count(), 2)

    def test_admin_update_category(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin update categories')
        data = {
            'current_name': 'Electronics',
            'new_name': 'Digital Electronics',
            'is_active': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Digital Electronics')
        self.assertFalse(self.category.is_active)

    def test_user_add_items_to_cart(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user add items to cart')
        data = [
            {
                'product_id': self.product.id,
                'quantity': 2
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 1)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 2)

    def test_get_products(self):
        url = reverse('search products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_categories(self):
        url = reverse('search categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_get_user_purchase(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user get purchase')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_user_carts(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user get carts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
