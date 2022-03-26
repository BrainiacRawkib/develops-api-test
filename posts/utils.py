from apiutils.utils import logger, generate_code
from .constraint_checks import check_if_user_has_voted_before
from .models import Post, Comment


# Create Actions
def create_post(title, author, content):
    try:
        return Post.objects.create(
            code='POST_' + generate_code('posts', 'Post'),
            title=title,
            author=author,
            content=content
        )

    except Exception as e:
        logger.error('create_post@Error')
        logger.error(e)
        return None


def create_comment(author, post, content):
    try:
        return Comment.objects.create(
            code='COM_' + generate_code('posts', 'Comment'),
            author=author,
            post=post,
            content=content
        )

    except Exception as e:
        logger.error('create_comment@Error')
        logger.error(e)
        return None


# Retrieve Actions
def retrieve_post(title):
    try:
        post = Post.objects.get(title=title)
        return post

    except Exception as e:
        logger.error('retrieve_post@Error')
        logger.error(e)
        return None


def retrieve_comment(code):
    try:
        return Comment.objects.get(code=code)

    except Exception as e:
        logger.error('retrieve_comment@Error')
        logger.error(e)
        return None


def retrieve_posts():
    try:
        return Post.objects.filter(is_deleted=False)

    except Exception as e:
        logger.error('retrieve_posts@Error')
        logger.error(e)
        return []


def retrieve_comments():
    try:
        return Comment.objects.filter(is_deleted=False)

    except Exception as e:
        logger.error('retrieve_comments@Error')
        logger.error(e)
        return []


# Update Actions
def update_post(post, validated_data):
    try:
        post.content = validated_data.get('content', post.content)
        post.up_votes = validated_data.get('up_votes', post.up_votes)
        post.down_votes = validated_data.get('down_votes', post.down_votes)
        post.save()
        return post

    except Exception as e:
        logger.error('update_post@Error')
        logger.error(e)
        return None


def vote_post(post, user, action):
    try:
        if not check_if_user_has_voted_before(user):
            return False

        if action == 'upvote':
            post.up_votes.add(user)
            post.save()
            return post
        elif action == 'downvote':
            post.down_votes.add(user)
            post.save()
            return post
        else:
            return post

    except Exception as e:
        logger.error('vote_post@Error')
        logger.error(e)
        return None

def update_comment(comment, validated_data):
    try:
        comment.content = validated_data.get('content', comment.content)
        comment.save()
        return comment

    except Exception as e:
        logger.error('update_comment@Error')
        logger.error(e)
        return None


# Delete Actions
def delete_post(post):
    try:
        post.is_deleted = True
        post.save()
        return True

    except Exception as e:
        logger.error('delete_post@Error')
        logger.error(e)
        return False


def delete_comment(comment):
    try:
        comment.is_deleted = True
        comment.save()
        return comment

    except Exception as e:
        logger.error('delete_comment@Error')
        logger.error(e)
        return None
