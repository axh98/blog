from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
from ckeditor.fields import RichTextField
# Create your models here.


class Comment(models.Model):
    # ForeignKey    多对一
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    body = RichTextField()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body[:20]
