from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_like = models.BooleanField(default=True)
