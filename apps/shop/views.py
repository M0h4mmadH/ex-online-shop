from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Product, ProductCategory
from .selectors import (search_products, search_categories, update_product, create_product, update_category,
                        create_category, process_add_items_to_cart, get_user_purchase_receipts, get_user_open_carts)

from .serializers import (OutGetProducts, InGetProducts, InGetCategories, OutGetCategories, InAdminUpdateProducts,
                          OutAdminCreateProducts, InAdminCreateProducts, OutAdminUpdateProducts, InAdminUpdateCategory,
                          OutAdminCreateCategory, InAdminCreateCategory, InUserAddItemsToCart, OutUserCart, OutCartItem,
                          InGetUserCarts, OutGetUserCarts, OutPurchaseReceiptSerializer, InUserCommentProducts,
                          OutUserCommentProducts)
from .services import create_user_comment

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


class UserAddAddress(APIView):
    def post(self, request):
        pass


class UserDeleteAddress(APIView):
    def post(self, request):
        pass


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
