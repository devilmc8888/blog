from django import template
from ..models import *
from django.db.models.aggregates import Count

register = template.Library()
#最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]
#定义归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')
#分类模板标签
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
#这个 Category.objects.annotate 方法和 Category.objects.all 有点类似，它会
# 返回数据库中全部 Category 的记录，但同时它还会做一些额外的事情，在这里我
# 们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文
# 章数。代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联
# 的模型参数名（这里是 Post，通过 ForeignKey 关联的），然后它便会统计
# Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章
# 数，最后把这个值保存到 num_posts 属性中。