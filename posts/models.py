from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from users.models import User


class Post(models.Model):
    code = models.CharField(max_length=25)
    title = models.CharField(max_length=254, unique=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    link = models.URLField()
    up_votes = models.ManyToManyField(User, related_name='users_upvotes',)
    down_votes = models.ManyToManyField(User, related_name='users_downvotes',)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    code = models.CharField(max_length=25, unique=True)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    content = models.TextField()
