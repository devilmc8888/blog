from django.db import models
# django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField('标题',max_length=70)
    body = models.TextField('文章内容')
    created_time = models.DateTimeField('发布时间',auto_now_add=True)
    modified_time = models.DateTimeField('修改时间',auto_now=True)
    excerpt = models.CharField('摘要',max_length=200, blank=True)
    category = models.ForeignKey(to=Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)# 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    views = models.PositiveIntegerField('阅读',default=0)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views']) #使用update_fields参数来告诉Django只更新数据库中 views 字段的值，以提高效率。
    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)