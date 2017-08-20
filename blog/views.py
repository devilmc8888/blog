from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from comments.forms import CommentForm
import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #分页
from django.views.generic import ListView #引用类视图
from django.db.models import Q #Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑
# Create your views here.
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/index.html', context={'post_list': posts,'page_totalNum':paginator.num_pages})
# class IndexView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#     paginate_by = 2
def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views() #调用统计浏览数的函数
    post.body = markdown.markdown(post.body,
                                  extensions=[ #对markdown语法的推展
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite', #语法高亮
                                      'markdown.extensions.toc', #允许我们自动生成目录
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)) #i 不区分大小写
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})
