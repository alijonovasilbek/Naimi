from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser


from .permissons import Cheak
from .serializers import RegistrationSerializer, VerificationSerializer, CitySerializer, ProfileSerializer, \
    LoginSerializer
from .models import PhoneVerification, User, City, ProfileModel
from .utils import send_sms
from rest_framework.viewsets import ModelViewSet


class CityView(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class RegisterView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            verification = PhoneVerification.objects.create(phone=phone)
            verification.generate_code()
            # send_sms(phone, f"Your verification code is {verification.code}")
            request.session['phone'] = phone
            request.session['city'] = serializer.validated_data['city'].id
            return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            if get_user_model().objects.filter(phone=phone).exists():
                verification = PhoneVerification.objects.create(phone=phone)
                verification.generate_code()
                return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You have to register first'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(CreateAPIView):
    serializer_class = VerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            try:
                otp = PhoneVerification.objects.get(phone=phone, code=code, is_active=True)
                print(otp)
                if otp.created_at >= timezone.now() - timedelta(minutes=2):
                    otp.is_active = False
                    otp.save()
                    city_id = request.session.get('city')

                    city = City.objects.get(id=city_id)
                    try:
                        user = User.objects.create_user(phone=phone, city=city)
                    except:
                        return Response(data={"msg": "Already checked"}, status=status.HTTP_400_BAD_REQUEST)

                    refresh = RefreshToken.for_user(user)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'message': 'Registration successful!'
                    }, status=status.HTTP_200_OK)
                else:
                    otp.is_active = False
                    otp.save()
                    return Response(data={"msg": "This code was used or invalid"})
            except PhoneVerification.DoesNotExist:
                return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneTokenObtainView(CreateAPIView):
    serializer_class = VerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            try:
                otp = PhoneVerification.objects.get(phone=phone, code=code, is_active=True)
                if otp.created_at >= timezone.now() - timedelta(minutes=2):
                    otp.is_active = False
                    otp.save()
                    user = User.objects.get(phone=phone)

                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    otp.is_active = False
                    otp.save()
                    return Response(data={"msg": "This code was used or invalid"})
            except (PhoneVerification.DoesNotExist, User.DoesNotExist):
                return Response({'error': 'Invalid phone number or verification code'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [Cheak, ]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        if ProfileModel.objects.filter(user_id=request.user).exists():
            return Response(data={'msg': 'You are already registered'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
