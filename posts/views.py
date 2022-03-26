from apiutils.views import http_response
from rest_framework.views import APIView
from rest_framework import status

from users.utils import get_user_by_access_token
from .serializers import PostSerializer, CommentSerializer
from .utils import (retrieve_post, retrieve_posts, retrieve_comment, retrieve_comments,
                    delete_post, delete_comment, vote_post)


class PostAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return http_response(
                'Bad Request. Access Token missing.',
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_user_by_access_token(token)
        if not user:
            return http_response(
                'Session Expired. Login Again',
                status=status.HTTP_408_REQUEST_TIMEOUT
            )

        query_params = request.query_params
        post_title = query_params['title']
        post = retrieve_post(post_title)

        if post:
            serializer = PostSerializer(post)
            if not post:
                return http_response(
                    'Post not found.',
                    status=status.HTTP_404_NOT_FOUND
                )
            return http_response(
                'Post Retrieved.',
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        posts = retrieve_posts()
        serializer = PostSerializer(posts, many=True)
        return http_response(
            'Posts Retrieved',
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return http_response(
                'Bad Request. Access Token missing.',
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_user_by_access_token(token)
        if not user:
            return http_response(
                'Session Expired. Login Again',
                status=status.HTTP_408_REQUEST_TIMEOUT
            )

        payload = request.data
        serializer = PostSerializer(data=payload)

        if serializer.is_valid():
            data = serializer.validated_data
            created_post, _ = serializer.create(data)

            if not created_post:
                return http_response(
                    'Server Error',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return http_response(
                'Post Created',
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        return http_response(
            'Bad Request',
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return http_response(
                'Bad Request. Access Token missing.',
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_user_by_access_token(token)
        if not user:
            return http_response(
                'Session Expired. Login Again',
                status=status.HTTP_408_REQUEST_TIMEOUT
            )

        payload = request.data
        post = retrieve_post(payload['title'])
        serializer = PostSerializer(data=payload)

        if serializer.is_valid():
            data = serializer.validated_data
            updated_post, _ = serializer.update(post, data)
            if not updated_post:
                return http_response(
                    'Error Updating Post.',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return http_response(
                'Post Successfully Updated.',
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        return http_response(
            'Bad Request',
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return http_response(
                'Bad Request. Access Token missing.',
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_user_by_access_token(token)
        if not user:
            return http_response(
                'Session Expired. Login Again',
                status=status.HTTP_408_REQUEST_TIMEOUT
            )

        query_params = request.query_params
        action = query_params['action']
        payload = request.data
        post = retrieve_post(payload['title'])
        serializer = PostSerializer(data=payload)

        if serializer.is_valid():
            data = serializer.validated_data

            if action == 'upvote':
                p = vote_post(post, user, action)
                updated_post, _ = serializer.update(p, data)
                if not updated_post:
                    return http_response(
                        'Error Upvoting Post.',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                return http_response(
                    'Post Successfully Upvoted.',
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
            elif action == 'downvote':
                p = vote_post(post, user, action)
                updated_post, _ = serializer.update(p, data)

                if not updated_post:
                    return http_response(
                        'Error DownVoting Post.',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                return http_response(
                    'Post Successfully DownVoted.',
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
            else:
                updated_post, _ = serializer.update(post, data)
                if not updated_post:
                    return http_response(
                        'Error Updating Post.',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                return http_response(
                    'Post Successfully Updated.',
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
        return http_response(
            'Bad Request',
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        query_params = request.query_params
        post_title = query_params['title']
        post = retrieve_post(post_title)

        if not post:
            return http_response(
                'Post not found',
                status=status.HTTP_404_NOT_FOUND
            )

        delete_post(post)
        return http_response(
            'Post successfully deleted.',
            status=status.HTTP_204_NO_CONTENT
        )


class CommentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        comment_code = query_params['code']
        comment = retrieve_comment(comment_code)

        if comment:
            serializer = CommentSerializer(comment)
            if not comment:
                return http_response(
                    'Comment not found.',
                    status=status.HTTP_404_NOT_FOUND
                )
            return http_response(
                'Comment Retrieved.',
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        comments = retrieve_comments()
        serializer = CommentSerializer(comments, many=True)
        return http_response(
            'Comments Retrieved',
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = CommentSerializer(data=payload)

        if serializer.is_valid():
            data = serializer.validated_data
            created_comment, _ = serializer.create(data)

            if not created_comment:
                return http_response(
                    'Server Error',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return http_response(
                'Comment Created',
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        return http_response(
            'Bad Request',
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, *args, **kwargs):
        query_params = request.query_params
        comment = retrieve_comment(query_params['code'])
        serializer = CommentSerializer(data=comment)

        if serializer.is_valid():
            data = serializer.validated_data
            updated_post, _ = serializer.update(comment, data)
            if not updated_post:
                return http_response(
                    'Error Updating Comment.',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return http_response(
                'Comment Successfully Updated.',
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        return http_response(
            'Bad Request',
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        query_params = request.query_params
        comment_code = query_params['code']
        comment = retrieve_comment(comment_code)

        if not comment:
            return http_response(
                'Comment not found',
                status=status.HTTP_404_NOT_FOUND
            )

        delete_comment(comment)
        return http_response(
            'Comment successfully deleted.',
            status=status.HTTP_204_NO_CONTENT
        )
