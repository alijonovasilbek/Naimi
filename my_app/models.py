from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random
import string


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        db_table = 'City_table'


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, city):
        if not phone:
            raise ValueError("Userda tel raqam bo'lishi kerak")
        user = self.model(phone=phone, city=city)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, city):
        user = self.create_user(phone, city)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone = models.CharField(max_length=255, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['city']

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'User'
        db_table = 'User_table'

    @property
    def is_staff(self):
        return self.is_admin

class PhoneVerification(models.Model):
    phone = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone} - {self.code}'

    def generate_code(self):
        self.code = ''.join(random.choices(string.digits, k=6))
        self.save()

#
#
# class Profile(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     bio = models.TextField()
#     image = models.ImageField(upload_to="profile")
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.first_name
#
#     class Meta:
#         verbose_name='Profile'
#         db_table='Profile_table'
#
#
# class ProfileImage(models.Model):
#     image = models.ImageField(upload_to="profile")
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.profile.first_name
#
#     class Meta:
#         verbose_name='ProfileImage'
#         db_table='ProfileImage_table'
#
#
# class ProfileVideo(models.Model):
#     video = models.FileField(upload_to='profile_video')
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.profile.first_name
#
#     class Meta:
#         verbose_name='ProfileVideo'
#         db_table='ProfileVideo_table'
#
#
# class Favourite(models.Model):
#     owner = models.ForeignKey(Profile, related_name='favourites', on_delete=models.CASCADE)
#     profiles = models.ForeignKey(Profile, related_name='favourited_by', on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name='Favourite'
#         db_table='Favourite_table'
#
#
