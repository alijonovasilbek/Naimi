from rest_framework import serializers

from app_category.models import SubCategory
from .models import FeedbackModel, FAQModel, FeedbackImageModel


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModel
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImageModel
        fields = '__all__'


class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQModel
        fields = '__all__'


class GetFeedbackWithSubIdSerializer(serializers.ModelSerializer):
    msg = serializers.SerializerMethodField(method_name='get_msg', read_only=True)
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)

    class Meta:
        model = SubCategory
        fields = ['msg', 'comments']

    def get_msg(self, obj):
        return 'successfully'

    def get_comments(self, obj):
        pass
