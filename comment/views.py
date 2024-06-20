from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import FeedbackModel, FAQsModel, FeedbackImageModel
from .permissions import IsAdminOrReadOnly
from .serializers import FeedbackSerializer, FAQsSerializer, FeedbackImageSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = FeedbackModel.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(to_user=self.request.data.get('service'), owner=self.request.user)


class FeedbackImageViewSet(viewsets.ModelViewSet):
    queryset = FeedbackImageModel.objects.all()
    serializer_class = FeedbackImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FAQsViewSet(viewsets.ModelViewSet):
    queryset = FAQsModel.objects.all()
    serializer_class = FAQsSerializer
    permission_classes = [IsAdminOrReadOnly]

