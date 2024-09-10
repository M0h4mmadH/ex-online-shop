from rest_framework import serializers

from apps.shop.models import *


class InGetProducts(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    min_price = serializers.IntegerField(required=False, min_value=0)
    max_price = serializers.IntegerField(required=False, min_value=0)
    order_by = serializers.ChoiceField(choices=['name', 'price', '-name', '-price'], required=False)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name']


class OutGetProducts(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created', 'updated', 'is_active']


class InGetCategories(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    order_by = serializers.ChoiceField(choices=['name', '-name'], required=False)


class OutGetCategories(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name']


class InGetUserOrders(serializers.ModelSerializer):
    pass


class OutGetUserOrders(serializers.ModelSerializer):
    pass


class InGetUserCards(serializers.ModelSerializer):
    pass


class OutGetUserCards(serializers.ModelSerializer):
    pass


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


class InCommentProducts(serializers.ModelSerializer):
    pass


class OutCommentProducts(serializers.ModelSerializer):
    pass


class InUserAddAddress(serializers.ModelSerializer):
    pass


class OutUserAddAddress(serializers.ModelSerializer):
    pass


class InUserAddItemsToCard(serializers.ModelSerializer):
    pass


class OutUserAddItemsToCard(serializers.ModelSerializer):
    pass


class InUserDeleteAddress(serializers.ModelSerializer):
    pass


class OutUserDeleteAddress(serializers.ModelSerializer):
    pass
