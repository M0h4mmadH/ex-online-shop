from rest_framework import status
from rest_framework.permissions import IsAdminUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Product
from .selectors import search_products, search_categories, update_product, create_product
from .serializers import (OutGetProducts, InGetProducts, InGetCategories, OutGetCategories, InAdminUpdateProducts,
                          OutAdminCreateProducts, InAdminCreateProducts, OutAdminUpdateProducts)
from ..utils.paginations import DefaultPagination


class GetProducts(APIView):
    permission_classes = []
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = DefaultPagination

    def get(self, request):
        input_serializer = InGetProducts(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        try:
            queryset = search_products(input_serializer.validated_data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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

        try:
            queryset = search_categories(input_serializer.validated_data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = OutGetCategories(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)


class GetUserOrders(APIView):
    def get(self, request):
        pass


class GetUserCards(APIView):
    def get(self, request):
        pass


class PurchaseOrders(APIView):
    def post(self, request):
        pass


class AdminCreateProducts(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = InAdminCreateProducts(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = create_product(serializer.validated_data)
            out_serializer = OutAdminCreateProducts(product)
            return Response(out_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:  # todo: make Exceptions more specific
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AdminUpdateProducts(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        product_id = request.data.get('id')
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InAdminUpdateProducts(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = update_product(product_id, serializer.validated_data)
            out_serializer = OutAdminUpdateProducts(product)
            return Response(out_serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SearchProducts(APIView):
    def get(self, request):
        pass


class CommentProducts(APIView):
    def post(self, request):
        pass


class UserAddAddress(APIView):
    def post(self, request):
        pass


class UserAddItemsToCard(APIView):
    def post(self, request):
        pass


class UserDeleteAddress(APIView):
    def post(self, request):
        pass
