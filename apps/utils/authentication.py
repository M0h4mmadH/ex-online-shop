from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, email=None, phone_number=None, password=None, **kwargs):
        user = None
        if email is None and phone_number is None:
            return user

        user_model = get_user_model()
        try:
            if email is not None:
                user = user_model.objects.get(email=email)
            elif phone_number is not None:
                user = user_model.objects.get(phone_number=phone_number)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
