from django.contrib import admin

# Register your models here.
from  .models import  (City,User)

admin.site.register(City)
admin.site.register(User)
# admin.site.register(Favourite)
# admin.site.register(ProfileImage)
# admin.site.register(Profile)
# admin.site.register(ProfileVideo)

