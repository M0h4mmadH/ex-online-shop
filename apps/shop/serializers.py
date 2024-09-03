from rest_framework import serializers


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
    pass


class OutAdminCreateProducts(serializers.ModelSerializer):
    pass


class InAdminUpdateProducts(serializers.ModelSerializer):
    pass


class OutAdminUpdateProducts(serializers.ModelSerializer):
    pass


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
