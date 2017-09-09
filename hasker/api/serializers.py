from rest_framework import serializers
from qa.models import Question


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'text', 'pub_date', 'author', 'rating')
