from django.contrib import admin

from .models import FAQsModel, FeedbackModel, FeedbackImageModel

admin.site.register(FeedbackModel)
admin.site.register(FAQsModel)
admin.site.register(FeedbackImageModel)
