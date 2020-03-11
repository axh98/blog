from django.contrib import admin

# Register your models here.
from .models import ArticlePost, ArticleColumn

# 在这里注册可以在管理后台查看
admin.site.register(ArticlePost)
admin.site.register(ArticleColumn)