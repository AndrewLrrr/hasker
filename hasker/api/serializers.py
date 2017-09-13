from rest_framework import serializers
from qa.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S', read_only=True)
    rating = serializers.IntegerField(read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Question
        fields = ('title', 'text', 'rating', 'pub_date', 'author', 'correct_answer', 'tags')
