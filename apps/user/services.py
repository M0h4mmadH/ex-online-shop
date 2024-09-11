import random
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.contrib.auth import get_user_model


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def validate_login(login, password):
    if '@' in login:
        user = authenticate(email=login, password=password)
    elif login.isnumeric():
        user = authenticate(phone_number=login, password=password)
    else:
        user = None
    return user


def generate_otp():
    return str(random.randint(100000, 999999))


def store_otp(key, otp):
    cache.set(key, otp, timeout=600)


def send_otp(validated_data):
    otp = generate_otp()
    if validated_data.get('email'):
        store_otp(validated_data['email'], otp)
        send_email_otp(validated_data['email'], otp)
    elif validated_data.get('phone_number'):
        store_otp(validated_data['phone_number'], otp)
        send_sms_otp(validated_data['phone_number'], otp)

    cache_key = f"registration_{otp}"
    cache.set(cache_key, validated_data, timeout=600)
    return otp


def verify_otp(validated_data):
    otp = validated_data['otp']
    login = validated_data['login']  # email or phone number
    stored_otp = cache.get(login)
    registration_data = None
    if stored_otp and stored_otp == otp:
        cache_key = f"registration_{otp}"
        registration_data = cache.get(cache_key)
        cache.delete(cache_key)

    return registration_data


def login_user(validated_data):  # todo : replace validated data in services and selectors with actual values they need
    login = validated_data['login']
    password = validated_data['password']
    user = validate_login(login, password)
    if user:
        tokens = generate_tokens_for_user(user)
        return tokens
    return None


def send_email_otp(email, otp):
    print(f"Sending OTP {otp} to email: {email}")


def send_sms_otp(phone_number, otp):
    print(f"Sending OTP {otp} to phone number: {phone_number}")
