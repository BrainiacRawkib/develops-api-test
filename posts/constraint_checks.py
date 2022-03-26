from apiutils.utils import logger


def check_if_user_has_voted_before(user):
    try:
        if user.users_upvotes.count() == 1 or user.users_downvotes.count() == 1:
            return False
        return True

    except Exception as e:
        logger.error('check_if_user_has_voted_before@Error')
        logger.error(e)
        return False
