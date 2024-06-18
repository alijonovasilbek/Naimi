from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, VerificationSerializer,CitySerializer
from .models import PhoneVerification, User, City
from .utils import send_sms
from rest_framework.viewsets import ModelViewSet


class CityView(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            verification, created = PhoneVerification.objects.get_or_create(phone=phone)
            verification.generate_code()
            # send_sms(phone, f"Your verification code is {verification.code}")
            request.session['phone'] = phone
            request.session['city'] = serializer.validated_data['city'].id
            return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(APIView):
    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            try:
                verification = PhoneVerification.objects.get(phone=phone, code=code)
                city_id = request.session.get('city')

                city = City.objects.get(id=city_id)
                user = User.objects.create_user(phone=phone, city=city)

                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'Registration successful!'
                }, status=status.HTTP_200_OK)
            except PhoneVerification.DoesNotExist:
                return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneTokenObtainView(APIView):
    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            try:
                verification = PhoneVerification.objects.get(phone=phone, code=code)
                user = User.objects.get(phone=phone)

                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except (PhoneVerification.DoesNotExist, User.DoesNotExist):
                return Response({'error': 'Invalid phone number or verification code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
