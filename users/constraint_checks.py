"""DB Constraint Checks For User Model."""
from apiutils.utils import logger
from .models import User


"""CREATING A USER."""
def check_user_create_details(*args, **kwargs):
    """
    Check the payload request details to see if some Unique constraints
    already exists.
    """
    try:
        if User.objects.filter(username=kwargs['username']).exists():
            return False
        if User.objects.filter(email=kwargs['email']).exists():
            return False
        return True

    except Exception as e:
        logger.error('check_user_payload_detail@Error')
        logger.error(e)
        return False


"""UPDATING A USER."""
def check_user_update_details(user_ins):
    """Check if user update details exists, exempting the requesting user fields (username, email, contact)."""
    try:
        if User.objects.exclude(username=user_ins.username).filter(username=user_ins.username).exists():
            return False
        if User.objects.exclude(email=user_ins.email).filter(email=user_ins.email).exists():
            return False
        return True

    except Exception as e:
        logger.error('check_user_update_details@Error')
        logger.error(e)
        return False