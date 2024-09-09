from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .selectors import search_products, search_categories
from .serializers import (OutGetProducts, InGetProducts, InGetCategories, OutGetCategories)
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
            return Response( status=status.HTTP_400_BAD_REQUEST)

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
    def post(self, request):
        pass


class AdminUpdateProducts(APIView):
    def post(self, request):
        pass


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
