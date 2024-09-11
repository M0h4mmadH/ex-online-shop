from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from .serializers import (
    UserRegisterInputSerializer,
    UserRegisterOutputSerializer,
    UserLoginInputSerializer,
    UserLoginOutputSerializer,
    OTPVerificationSerializer,
)
from . import selectors, services
from .services import send_otp, verify_otp, login_user


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        input_serializer = UserRegisterInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        send_otp(input_serializer.validated_data)
        return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registration_data = verify_otp(serializer.validated_data)
        if registration_data is None:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        user = selectors.create_user(**registration_data)
        output_serializer = UserRegisterOutputSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        input_serializer = UserLoginInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        tokens = login_user(input_serializer.validated_data)
        if tokens is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        output_serializer = UserLoginOutputSerializer(tokens)
        return Response(output_serializer.data)
