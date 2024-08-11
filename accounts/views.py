from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import User, OTP, LoginAttempt
from .serializers import UserSerializer, OTPSerializer, PhoneSerializer, LoginSerializer
import random
from rest_framework import generics
from rest_framework.authtoken.models import Token


class EnterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self , request):
        serializer = PhoneSerializer(data = request.data)
        if serializer.is_valid():
            user = User.objects.filter(phone_number=serializer.data['phone_number']).first()
            if user:
                return Response({"message": "User exist."}, status=status.HTTP_200_OK)
            else:
                # otp = ''.join(random.choices('0123456789', k=6))
                ########################## for test 
                otp = '123456'
                OTP.objects.create(phone_number=serializer.data['phone_number'], code=otp)
                # send SMS include code for signup
                return Response({"message": "OTP sent"}, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        otpSerializer = OTPSerializer(data={"phone_number":request.data.get('phone_number'),
                                            "code": request.data.get('code')})

        userSerializer = UserSerializer(data = {"username":request.data.get('phone_number'),"first_name":request.data.get('first_name'),
                                            "last_name": request.data.get('last_name'),"email":request.data.get('email'),
                                            "password":request.data.get('password'),})

        if otpSerializer.is_valid() and userSerializer.is_valid():
            otp_entry = OTP.objects.filter(phone_number=otpSerializer.data['phone_number'], code=otpSerializer.data['code']).first()
            if otp_entry and not otp_entry.is_expired():
                user = User.objects.create_user( phone_number = otpSerializer.data['phone_number'] , username = userSerializer.data['username'],
                                                            first_name = userSerializer.data['first_name'], last_name = userSerializer.data['last_name'],
                                                            email = userSerializer.data['email'], password = userSerializer.data['password'])
                if user:
                    return Response({"message": "User created."}, status=status.HTTP_201_CREATED)
                return Response({"message": "User exists. Please login."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response( userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data = request.data)
        ip_address = request.META.get('REMOTE_ADDR')

        if serializer.is_valid():

            login_attempt = LoginAttempt.objects.filter(phone_number=serializer.data['phone_number'], ip_address=ip_address).first()
            if login_attempt and login_attempt.blocked_until and login_attempt.blocked_until > timezone.now():
                return Response({"error": "Too many failed attempts. Try later."}, status=status.HTTP_403_FORBIDDEN)

            user = authenticate(username=serializer.data["phone_number"], password=serializer.data['password'])
            if user:
                return Response({"user login successfully!!"}, status=status.HTTP_200_OK)
            else:
                if login_attempt:
                    login_attempt.attempts += 1
                    if login_attempt.attempts >= 3:
                        login_attempt.blocked_until = timezone.now() + timezone.timedelta(hours=1)
                    login_attempt.save()
                else:
                    LoginAttempt.objects.create(phone_number=serializer.data['phone_number'], ip_address=ip_address, attempts=1)
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
