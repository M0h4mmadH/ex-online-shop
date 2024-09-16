from django.db.models import Sum
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.user.models import User
from .models import (ProductCategory, Product, Cart, CartItem, PurchaseReceipt, Order, ReceiptOrder, Comment,
                     UserRateProduct, Address, City)


class ShopAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin@test.com', 'adminpass')
        self.regular_user = User.objects.create_user('user@test.com', 'userpass')
        self.category = ProductCategory.objects.create(name='Electronics')
        self.product = Product.objects.create(name='Laptop', description='A good laptop', price=1000,
                                              category=self.category)
        self.city = City.objects.create(name='Tehran')
        self.city2 = City.objects.create(name='San Francisco')

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

    def test_user_add_a_item_to_cart(self):
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

    def test_user_add_more_than_ten_items_to_cart(self):
        # Create products
        self.client.force_authenticate(user=self.regular_user)
        for i in range(0, 10):
            product = {
                'name': f"Product {i}",
                'price': (i + 1) * 100,
                'category': self.category,
            }
            Product.objects.create(**product)

        # Add item to active cart
        url = reverse('user add items to cart')
        product_ids = Product.objects.values_list('id', flat=True)
        self.assertGreater(len(product_ids), 0)

        product_data = []
        for product_id in product_ids:
            product_data.append({
                'product_id': product_id,
                'quantity': 2
            })
        response = self.client.post(url, product_data, format='json')

        # Testing results
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Too many items")

    def test_user_add_exactly_ten_items_to_cart(self):
        # Create products
        self.client.force_authenticate(user=self.regular_user)
        for i in range(0, 9):
            product = {
                'name': f"Product {i}",
                'category': self.category,
                'price': (i + 1) * 100,
            }
            Product.objects.create(**product)

        # Add item to active cart
        url = reverse('user add items to cart')
        product_ids = Product.objects.values_list('id', flat=True)
        self.assertGreater(len(product_ids), 0)

        product_data = []
        for product_id in product_ids:
            product_data.append({
                'quantity': 1,
                'product_id': product_id,
            })
        response = self.client.post(url, product_data, format='json')

        # Testing results
        cart = Cart.objects.get(user=self.regular_user)
        cart_products_count = cart.cartitem_set.aggregate(Sum('quantity'))['quantity__sum'] or 0
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart_products_count, 10)

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

    def test_user_valid_comment_product(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user comment product')
        comment = 'best product ever!'
        data = {
            'comment': comment,
            'product_id': self.product.id,
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.filter(comment=comment).count(), 1)

    def test_user_invalid_comment_product(self):
        self.client.force_authenticate(user=self.regular_user)
        comment = 'invalid comment'
        url = reverse('user comment product')
        data = {
            'comment': comment,
            'product_id': self.product.id * 3,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.filter(comment=comment).count(), 0)

    def test_user_valid_rate_product(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user rate product')
        data = {
            'product_id': self.product.id,
            'rate': 5,
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserRateProduct.objects.count(), 1)

    def test_user_invalid_rate_product(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user rate product')
        data = {
            'product_id': self.product.id,
            'rate': 50,
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserRateProduct.objects.count(), 0)

    def test_user_multiple_rate_product(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user rate product')
        self.client.post(path=url, data={
            'product_id': self.product.id,
            'rate': 1,
        }, format='json')
        self.client.post(path=url, data={
            'product_id': self.product.id,
            'rate': 2,
        }, format='json')
        self.client.post(path=url, data={
            'product_id': self.product.id,
            'rate': 3,
        }, format='json')
        response = self.client.post(path=url, data={
            'product_id': self.product.id,
            'rate': 4,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserRateProduct.objects.count(), 1)
        self.assertEqual(UserRateProduct.objects.first().rate, 4)

    def test_user_create_valid_address(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user create address')
        address = 'javahad - fatemi - tehran - iran - earth'
        data = {
            'address': address,
            'city': self.city.name
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.first().address, address)

    def test_user_create_invalid_lengthy_address(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user create address')
        address = 'javahad - fatemi - tehran - iran - earth',
        data = {
            'address': address * 20,
            'city': self.city.name
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Address.objects.count(), 0)

    def test_user_address_update_with_valid_address(self):
        url = reverse('user create address')
        self.client.force_authenticate(user=self.regular_user)
        address = 'javahad - fatemi - tehran - iran - earth'
        new_address = 'mars'
        data = {
            'address': address,
            'city': self.city.name
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('user update address')
        address_id = response.data['id']
        data = {
            'address_id': address_id,
            'new_address': new_address
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.first().address, new_address)

    def test_user_address_update_valid_city(self):
        url = reverse('user create address')
        self.client.force_authenticate(user=self.regular_user)
        address = 'javahad - fatemi - tehran - iran - earth'
        data = {
            'city': self.city.name,
            'address': address
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('user update address')
        address_id = response.data['id']
        data = {
            'address_id': address_id,
            'new_city': self.city2.name
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.first().city.name, self.city2.name)

    def test_user_address_update_with_invalid_lengthy_address(self):
        self.client.force_authenticate(user=self.regular_user)
        address = 'javahad - fatemi - tehran - iran - earth'
        url = reverse('user create address')
        new_address = 'mars - ' * 50
        data = {
            'city': self.city.name,
            'address': address,
        }
        response = self.client.post(path=url, data=data, format='json')

        address_id = response.data['id']
        url = reverse('user update address')
        data = {
            'new_address': new_address,
            'address_id': address_id,
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_address_update_with_invalid_city(self):
        url = reverse('user create address')
        self.client.force_authenticate(user=self.regular_user)
        address = 'javahad - fatemi - tehran - iran - earth'
        data = {
            'city': self.city.name,
            'address': address
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('user update address')
        address_id = response.data['id']
        data = {
            'address_id': address_id,
            'new_city': 'some unknown city name'
        }

        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_address_delete(self):
        url = reverse('user create address')
        self.client.force_authenticate(user=self.regular_user)
        address = 'javahad - fatemi - tehran - iran - earth'
        data = {
            'city': self.city.name,
            'address': address
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('user delete address')
        address_id = response.data['id']
        data = {
            'address_id': address_id,
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Address.objects.filter(is_active=True).count(), 0)

    def test_user_address_get_active_addresses(self):
        # Add two addresses
        url = reverse('user create address')
        self.client.force_authenticate(user=self.regular_user)
        active_address = 'some active address'
        deleted_address = 'some inactive address'
        data = {
            'address': active_address,
            'city': self.city.name,
        }
        self.client.post(path=url, data=data, format='json')
        data = {
            'address': deleted_address,
            'city': self.city2.name,
        }
        response = self.client.post(path=url, data=data, format='json')

        # Delete one address
        url = reverse('user delete address')
        address_id = response.data['id']
        data = {
            'address_id': address_id,
        }
        self.client.post(path=url, data=data, format='json')

        # Get the user address list
        url = reverse('user get address')
        address_response = self.client.get(path=url)
        db_active_address = Address.active.first()
        response = address_response.data[0]

        # Validate response
        self.assertEqual(address_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Address.active.all().count(), 1)
        self.assertEqual(response['id'], db_active_address.id)
        self.assertEqual(response['address'], db_active_address.address)
        self.assertEqual(response['city']['name'], db_active_address.city.name)

    def test_user_delete_cart(self):
        # Create cart with an item
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user add items to cart')
        data = [
            {
                'product_id': self.product.id,
                'quantity': 2
            }
        ]
        response = self.client.post(url, data, format='json')
        cart_id = response.data['cart']['id']

        # Delete cart
        url = reverse('user delete cart')
        response = self.client.post(path=url, data={'cart_id': cart_id}, format='json')

        # Validate results
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.active.count(), 0)

    def test_user_delete_non_exsting_cart(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user delete cart')
        response = self.client.post(path=url, data={'cart_id': 10}, format='json')

        # Validate results
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
