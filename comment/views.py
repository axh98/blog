from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .form import CommentForm
from .models import Comment
from article.models import ArticlePost
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            # new_comment.body = request.POST['body']
            # redirect   参数是 模型  ，调用该模型的   get_absolute_url()方法
            #                是 视图  ， 可以带有函数， 可以使用   urlresolvers.reverse   来反向解析名称
            #                是 绝对或相对的   URL  ，直接跳转
            return redirect(article)
        else:
            return HttpResponse('表单有误')
    else:
        return HttpResponse('仅接受POST')