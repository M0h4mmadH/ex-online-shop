from django.db.models import Q

from apps.user.models import User


def get_user_by_login(login):
    return User.objects.filter(
        Q(username=login) | Q(phone_number=login)
    ).first()


def create_user(password, email=None, phone_number=None):
    return User.objects.create_user(
        email=email,
        phone_number=phone_number,
        password=password
    )


def validate_login(login, password):
    user = User.objects.filter(Q(email=login) | Q(phone_number=login)).first()
    if user and user.check_password(password):
        return user
    return None
