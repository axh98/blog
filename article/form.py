from django import forms
from .models import ArticlePost


class ArticlePostForm(forms.ModelForm):
    # forms.ModelForm   适合于需要与数据库进行直接交互的，如增删改
    class Meta:
        # 指明数据来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'body', 'tags')