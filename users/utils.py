"""ABSTRACTING ALL DB OPERATIONS FROM API VIEWS."""
from apiutils.utils import logger, generate_code
from rest_framework.authtoken.models import Token
from .constraint_checks import check_user_update_details, check_user_create_details
from .models import User

"""DB OPERATIONS: CRUD OPERATIONS"""

"""CREATE"""

def create_user(username, email, password):
    """Create a new user."""
    try:
        if not check_user_create_details(username=username, email=email):
            return None
        return User.objects.create_user(
            code='USR_' + generate_code('users', 'User'),
            username=username,
            email=email,
            password=password,
        )

    except Exception as e:
        logger.error('create_user@Error')
        logger.error(e)
        return None


"""RETRIEVE"""

def get_user_by_username(username):
    """Retrieve a User by username"""
    try:
        if username:
            return User.objects.get(username=username)
        return None

    except Exception as e:
        logger.error('get_user_by_username@Error')
        logger.error(e)
        return None


def get_user_by_email(email):
    """Retrieve a User by email"""
    try:
        if email:
            return User.objects.get(email=email)
        return None

    except Exception as e:
        logger.error('get_user_by_email@Error')
        logger.error(e)
        return None


def get_all_users():
    """Get all Users."""
    try:
        users = User.objects.all()
        return users

    except Exception as e:
        logger.error('get_all_user@Error')
        logger.error(e)
        return []


def get_user_by_access_token(token):
    try:
        key = token.split()
        access_token = key[1]
        token = Token.objects.get(key=access_token)
        user = token.user
        if user and user.is_active:
            return user
        return None

    except Exception as e:
        logger.error('get_user_by_access_token@Error')
        logger.error(e)
        return None


"""UPDATE"""

def update_user(user_ins, validated_data):
    """Update user."""
    try:
        if not check_user_update_details(user_ins):
            return None
        user_ins.username = validated_data.get('username', user_ins.username)
        user_ins.email = validated_data.get('email', user_ins.email)
        user_ins.save()
        return user_ins

    except Exception as e:
        logger.error('update_user@Error')
        logger.error(e)
        return None


"""DELETE"""

def delete_user(user):
    """Delete a user."""
    try:
        user.is_active = False
        user.save()
        return True

    except Exception as e:
        logger.error('delete_user@Error')
        logger.error(e)
        return False


"""GENERATE TOKEN FOR USER"""
def generate_token_for_user(user):
    try:
        token = Token.objects.get_or_create(user)
        return token

    except Exception as e:
        logger.error('generate_token_for_user@Error')
        logger.error(e)
        return None