from rest_framework import serializers
from . import models


class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ('text',)


class ListTicketSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = models.Ticket
        fields = ('author', 'text', 'status', 'created_at')


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        exclude = ('support', 'created_at',)


class ChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ('status',)


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('answer', 'parent', 'text',)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentsListSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = models.Comment
        fields = ('id', 'user', 'text', 'children')


class AnswerSerializer(serializers.ModelSerializer):
    comments = CommentsListSerializer(many=True)
    support = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = models.Answer
        fields = ('support', 'text', 'created_at', 'comments')


class TicketDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    answer = AnswerSerializer(read_only=True, many=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = models.Ticket
        fields = ('author', 'text', 'status', 'created_at', 'answer')
