from rest_framework import serializers

from apps.shop.models import *


class InGetProducts(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    min_price = serializers.IntegerField(required=False, min_value=0)
    max_price = serializers.IntegerField(required=False, min_value=0)
    city = serializers.CharField(required=False, allow_blank=True)
    order_by = serializers.ChoiceField(choices=['name', 'price', '-name', '-price', 'city', '-city'], required=False)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name']


class ProductCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


class OutGetProducts(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    city = ProductCitySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created', 'updated', 'is_active', 'city']


class InGetCategories(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    order_by = serializers.ChoiceField(choices=['name', '-name'], required=False)


class OutGetCategories(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name']


class OutGetProductsForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class OutOrderSerializer(serializers.ModelSerializer):
    product = OutGetProductsForOrderSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'price', 'product', 'discount']


class OutPurchaseReceiptSerializer(serializers.ModelSerializer):
    items = OutOrderSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseReceipt
        fields = ['items', 'price', 'user']


class InGetUserCarts(serializers.Serializer):
    status = serializers.ChoiceField(choices=Cart.CART_STATUS, required=False)


class OutGetUserCarts(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'created', 'cart_status', 'products']


class InPurchaseOrders(serializers.ModelSerializer):
    pass


class OutPurchaseOrders(serializers.ModelSerializer):
    pass


class InAdminCreateProducts(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'is_active']

    @classmethod
    def validate_category(cls, value):
        try:
            return ProductCategory.objects.get(name=value)
        except ProductCategory.DoesNotExist:
            raise serializers.ValidationError("Invalid category")


class OutAdminCreateProducts(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created', 'updated', 'is_active']


class InAdminUpdateProducts(serializers.ModelSerializer):
    category = serializers.CharField(required=False)
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'is_active']
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'price': {'required': False},
            'is_active': {'required': False},
        }

    @classmethod
    def validate_category(cls, value):
        try:
            return ProductCategory.objects.get(name=value)
        except ProductCategory.DoesNotExist:
            raise serializers.ValidationError("Invalid category")


class InAdminCreateCategory(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name', 'is_active']


class OutAdminCreateCategory(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name', 'is_active']


class InAdminUpdateCategory(serializers.ModelSerializer):
    current_name = serializers.CharField(required=True)
    new_name = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)

    @classmethod
    def validate_new_name(cls, value):
        if ProductCategory.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return value

    class Meta:
        model = ProductCategory
        fields = ['current_name', 'new_name', 'is_active']


class OutAdminUpdateProducts(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created', 'updated', 'is_active']


class InSearchProducts(serializers.ModelSerializer):
    pass


class OutSearchProducts(serializers.ModelSerializer):
    pass


class InUserCommentProducts(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['product_id', 'comment']


class OutUserCommentUserID(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class OutUserCommentProducts(serializers.ModelSerializer):
    user_id = OutUserCommentUserID(read_only=True)

    class Meta:
        model = Comment
        fields = ['user_id']


class InUserRateProduct(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    rate = serializers.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = UserRateProduct
        fields = ['product_id', 'rate']


class InUserAddAddress(serializers.Serializer):
    address = serializers.CharField(max_length=250, required=True)
    city = serializers.CharField(max_length=50, required=True)


class InUserUpdateAddress(serializers.Serializer):
    address_id = serializers.IntegerField()
    new_address = serializers.CharField(max_length=250, required=False)
    new_city = serializers.CharField(max_length=50, required=False)


class InUserDeleteAddress(serializers.Serializer):
    address_id = serializers.IntegerField()


class OutUserGetAddressCity(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


class OutUserGetAddress(serializers.ModelSerializer):
    city = OutUserGetAddressCity(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'address', 'city']



class InUserAddItemsToCart(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class OutUserCart(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'cart_status', 'created']


class OutCartItem(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.IntegerField(source='product.price')

    class Meta:
        model = CartItem
        fields = ['id', 'product_name', 'product_price', 'quantity']
