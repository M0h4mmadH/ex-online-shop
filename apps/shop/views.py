from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import (Product, ProductCategory, Address, City, Cart)
from .selectors import (search_products, search_categories, update_product, create_product, update_category,
                        create_category, process_add_items_to_cart, get_user_purchase_receipts, get_user_open_carts)

from .serializers import (OutGetProducts, InGetProducts, InGetCategories, OutGetCategories, InAdminUpdateProducts,
                          OutAdminCreateProducts, InAdminCreateProducts, OutAdminUpdateProducts, InAdminUpdateCategory,
                          OutAdminCreateCategory, InAdminCreateCategory, InUserAddItemsToCart, OutUserCart, OutCartItem,
                          InGetUserCarts, OutGetUserCarts, OutPurchaseReceiptSerializer, InUserCommentProducts,
                          OutUserCommentProducts, InUserRateProduct, InUserAddAddress, InUserUpdateAddress,
                          InUserDeleteAddress, OutUserGetAddress, InUserDeleteCart)

from .services import (create_user_comment, create_or_update_user_product_rate, create_user_address,
                       update_user_address, inactive_user_address, delete_user_cart)
from ..utils.exceptions import TooManyItemsException

from ..utils.paginations import DefaultPagination


class GetProducts(APIView):
    permission_classes = []
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = DefaultPagination

    def get(self, request):
        input_serializer = InGetProducts(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        queryset = search_products(input_serializer.validated_data)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = OutGetProducts(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)


class GetCategories(APIView):
    permission_classes = []
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = DefaultPagination

    def get(self, request):
        input_serializer = InGetCategories(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        queryset = search_categories(input_serializer.validated_data)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = OutGetCategories(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)


class GetUserPurchaseReceipts(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OutPurchaseReceiptSerializer

    def get(self, request):
        receipts = get_user_purchase_receipts(request.user)
        output_serializer = self.serializer_class(receipts, many=True)
        return Response(output_serializer.data)


class GetUserActiveCarts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = InGetUserCarts(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        carts = get_user_open_carts(request.user, **serializer.validated_data)
        return Response(OutGetUserCarts(carts, many=True).data)


class PurchaseOrders(APIView):
    def post(self, request):
        pass


class AdminCreateProducts(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = InAdminCreateProducts(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = create_product(serializer.validated_data)
        out_serializer = OutAdminCreateProducts(product)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)


class AdminUpdateProducts(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = InAdminUpdateProducts(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = update_product(serializer.validated_data)
            out_serializer = OutAdminUpdateProducts(product)
            return Response(out_serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class AdminCreateCategory(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = InAdminCreateCategory(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = create_category(serializer.validated_data)
        out_serializer = OutAdminCreateCategory(category)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)


class AdminUpdateCategory(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = InAdminUpdateCategory(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            category = update_category(serializer.validated_data)
            out_serializer = OutAdminCreateCategory(category)
            return Response(out_serializer.data, status=status.HTTP_200_OK)
        except ProductCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


class UserCommentProducts(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        input_serializer = InUserCommentProducts(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            create_user_comment(user=request.user,
                                post=None,
                                comment=input_serializer.validated_data['comment'],
                                product_id=input_serializer.validated_data['product_id'],
                                )
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        output_serializer = OutUserCommentProducts(input_serializer.validated_data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class UserRateProducts(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        input_serializer = InUserRateProduct(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            create_or_update_user_product_rate(user=request.user,
                                               product_id=input_serializer.validated_data['product_id'],
                                               rate=input_serializer.validated_data['rate'])
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_201_CREATED)


class UserAddAddress(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        input_serializer = InUserAddAddress(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            address = create_user_address(user=request.user,
                                          city=input_serializer.validated_data['city'],
                                          address=input_serializer.validated_data['address'])
        except City.DoesNotExist:
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={'id': address.id}, status=status.HTTP_201_CREATED)


class UserUpdateAddress(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        input_serializer = InUserUpdateAddress(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            address = update_user_address(user=request.user,
                                          address_id=input_serializer.validated_data['address_id'],
                                          new_city=input_serializer.validated_data.get('new_city'),
                                          new_address=input_serializer.validated_data.get('new_address'))
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        except City.DoesNotExist:
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={'id': address.id}, status=status.HTTP_200_OK)

    def patch(self, request):
        return self.post(request)


class UserGetAddress(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    output_serializer = OutUserGetAddress

    def get(self, request):
        user_addresses = Address.active.filter(user=request.user)
        output_data = self.output_serializer(user_addresses, many=True)
        return Response(output_data.data, status=status.HTTP_200_OK)


class UserDeleteAddress(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        input_serializer = InUserDeleteAddress(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            inactive_user_address(user=request.user,
                                  address_id=input_serializer.validated_data['address_id'])
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"id": input_serializer.validated_data['address_id']}, status=status.HTTP_200_OK)


class UserAddItemsToCart(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = InUserAddItemsToCart(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        try:
            cart, cart_items = process_add_items_to_cart(request.user, serializer.validated_data)
            cart_serializer = OutUserCart(cart)
            items_serializer = OutCartItem(cart_items, many=True)
            return Response({
                'cart': cart_serializer.data,
                'items': items_serializer.data
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except TooManyItemsException:
            return Response({"error": "Too many items"}, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteCart(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    input_serializer_class = InUserDeleteCart

    def post(self, request):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            delete_user_cart(user=request.user, cart_id=input_serializer.validated_data['cart_id'])
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={"id": input_serializer.validated_data['cart_id']}, status=status.HTTP_200_OK)
