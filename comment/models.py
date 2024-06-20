from django.db import models
from users.models import ProfileModel


from app_service.models import Service

User = ProfileModel


class FeedbackModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner')
    msg = models.TextField()
    mark = models.IntegerField()
    created_at = models.DateField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service')

    def __str__(self):
        return f'Comment {self.pk} on Service {self.service}'

    class Meta:
        db_table = "feedback"


class FeedbackImageModel(models.Model):
    image = models.ImageField(upload_to='static/FeedbackImage/')
    comment = models.ForeignKey(FeedbackModel, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'CommentImage {self.pk} for Comment {self.comment}'

    class Meta:
        db_table = "FeedbackImage"


class FAQModel(models.Model):
    question = models.TextField()
    answer = models.TextField()
    role = models.BooleanField(default=False)

    def __str__(self):
        return f'QuestionAnswer {self.pk}'

    class Meta:
        db_table = "FAQs"
