from apiutils.views import http_response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
from .utils import *


class UserAPIView(APIView):
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
        username = query_params['username']

        if username:
            user = get_user_by_username(username)
            if user:
                serializer = UserSerializer(user)
                return http_response(
                    'User Retrieved',
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
            return http_response(
                'User not found',
                status=status.HTTP_404_NOT_FOUND,
            )

        users = get_all_users()
        serializer = UserSerializer(users, many=True)
        return http_response(
            'Users Retrieved',
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = UserSerializer(data=payload)
        if serializer.is_valid():
            data = serializer.validated_data
            created_user, _ = serializer.create(data)
            if created_user:
                return http_response(
                    'User created',
                    status=status.HTTP_201_CREATED,
                    data=serializer.data
                )
            return http_response(
                'Server Error',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=serializer.data
            )
        return http_response(
            'Bad Request',
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.data
        )

    def put(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return http_response(
                'Bad Request. Access Token missing.',
                status=status.HTTP_400_BAD_REQUEST
            )

        user =  get_user_by_access_token(token)
        payload = request.data

        if user:
            serializer = UserSerializer(data=payload)
            if serializer.is_valid():
                data = serializer.validated_data
                user_to_update, _ = serializer.update(user, data)
                if user_to_update:
                    return http_response(
                        'User updated.',
                           status=status.HTTP_200_OK,
                           data=serializer.data
                    )
                return http_response(
                    'Server Error',
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data=serializer.errors
                )
        return http_response(
                'User does not exist.',
                status=status.HTTP_404_NOT_FOUND,
                data=payload
            )

    def delete(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return http_response(
                'Bad Request. Access Token missing.',
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_user_by_access_token(token)

        if user:
            user_to_delete = delete_user(user)

            if user_to_delete:
                return http_response(
                    'User deleted.',
                    status=status.HTTP_204_NO_CONTENT,
                )
            return http_response(
                'User already deleted.',
                status=status.HTTP_404_NOT_FOUND
            )
        return http_response(
            'User not found.',
            status=status.HTTP_404_NOT_FOUND
        )


class LoginAPI(APIView):

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = LoginSerializer(data=payload)
        if serializer.is_valid():
            return http_response(
                'Login Successful.',
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        return http_response(
            'Invalid Credentials',
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        payload = request.data
        context = {'request': request}
        serializer = self.serializer_class(data=payload, context=context)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }
        return http_response(
            'Login Successful',
            status=status.HTTP_200_OK,
            data=data
        )
