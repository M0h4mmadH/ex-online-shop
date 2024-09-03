from rest_framework.views import APIView


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
