from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class ArticlePost(models.Model):
    # ForeignKey 定义的关系，每个或多个  ArticlePost  对象都关联到一个    User  对象
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    body = models.TextField()

    # PositiveIntegerField    存正整数
    total_view = models.PositiveIntegerField(default=0)

    create_time = models.DateTimeField(default=timezone.now)

    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # 按照   create_time    倒序排序  所以是   -
        #   元组   要有   ,
        #  提供模型的元数据   元数据是   “任何不是字段的东西”  如排序选项   ordering     数据库表名  db_name
        #  是整张表的共同行为
        ordering = ('-create_time',)

    def __str__(self):
        return self.title

    # 通过   reverse()  返回文章详情页的   url
    # comment  视图里用   article 做参数
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
