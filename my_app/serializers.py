from rest_framework import serializers
from .models import User, City, ProfileModel


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city')

    class Meta:
        model = User
        fields = ['phone', 'city_id']

    def create(self, validated_data):
        city = validated_data.pop('city')
        user = User.objects.create_user(phone=validated_data['phone'], city=city)
        return user


class VerificationSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=255)
    code = serializers.CharField(required=True, max_length=6)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = "__all__"
        extra_kwargs = {
            'user_id': {'read_only': True}
        }


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
