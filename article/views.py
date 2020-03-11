# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .form import ArticlePostForm
from .models import ArticlePost, ArticleColumn
from comment.models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import markdown


def article_list(request):
    #   在   url  末尾附上  ?key = value的键值对，视图中可通过   request.GET.get('key')   获取  value
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_view':
            #     icontains     不区分大小写     __  前面的是查询字段
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_view')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        #   若没有这句， 若用户没有搜索操作， 会使   search = None   传进去之后会变成字符串    不是空
        search = ''
        if order == 'total_view':
            article_list = ArticlePost.objects.all().order_by('-total_view')
        else:
            article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # context   这个就是传给模板的数据  即在前端可以使用的数据
    context = {'articles': articles, 'order': order, 'search': search}
    return render(request, 'article/list.html', context)


def article_detail(request, id=None):
    article = get_object_or_404(ArticlePost, id=id)
    article.total_view += 1
    comments = Comment.objects.filter(article=id)
    # print(comments)
    # update_fields    指明更新字段
    article.save(update_fields=['total_view'])
    md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',
                                                 'markdown.extensions.toc'])
    article.body = md.convert(article.body)
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            # 保存数据，  但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            #    指定   id = 1   为作者
            new_article.author = User.objects.get(id=request.user.id)
            #    将文章保存到数据库中
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse('表单数据有误，请重新填写')
    # 如果用户请求数据
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id=None):
    if request.method == 'POST':
        article = get_object_or_404(ArticlePost, id=id)
        if request.user != article.author:
            return HttpResponse('你没有权限删除文章')
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许POST请求')


@login_required(login_url='/userprofile/login/')
def article_update(request, id=None):
    article = get_object_or_404(ArticlePost, id=id)
    if article.author != request.user:
        return HttpResponse('你没有权限修改该文章')
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('表单内容有误，请重新填写')
    else:
        article_post_form = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)
