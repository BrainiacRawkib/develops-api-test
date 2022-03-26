from apiutils.utils import logger
from rest_framework import serializers
from .models import Post, Comment
from .utils import create_comment, create_post, update_comment, update_post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'code', 'title', 'author', 'content', 'link', 'up_votes', 'down_votes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['code']

    def create(self, validated_data):
        try:
            return create_post(**validated_data), ""

        except Exception as e:
            logger.error('PostSerializer.create@Error')
            logger.error(e)
            return None, str(e)

    def update(self, instance, validated_data):
        try:
            return update_post(instance, validated_data)

        except Exception as e:
            logger.error('PostSerializer.update@Error')
            logger.error(e)
            return None, str(e)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'code', 'author', 'post', 'created_at', 'content'
        ]
        read_only_fields = ['code']

    def create(self, validated_data):
        try:
            return create_comment(**validated_data), ""

        except Exception as e:
            logger.error('CommentSerializer.create@Error')
            logger.error(e)
            return None, str(e)

    def update(self, instance, validated_data):
        try:
            return update_comment(instance, validated_data), ""

        except Exception as e:
            logger.error('CommentSerializer.update@Error')
            logger.error(e)
            return None, str(e)
