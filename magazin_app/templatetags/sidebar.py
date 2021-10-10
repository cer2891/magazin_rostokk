from django import template
from django.db.models import Count, F
from magazin_app.models import Cart, Tag, Category

register = template.Library()


@register.inclusion_tag('magazin_app/list_categories.html')
def show_categories(arg1='', arg2=''):
    # categories = Category.objects.all()
    # categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)

    # categories = cache.get('categories')
    # if not categories:
    #     categories = Category.objects.annotate(
    #         cnt=Count('news', filter=F('news__is_published'))
    #     ).filter(cnt__gt=0)
    #     cache.set('categories', categories, 30)

    categories = Category.objects.annotate(
        cnt=Count('cart', filter=F('cart__is_published'))
    ).filter(cnt__gt=0)
    return {"categories": categories, 'arg1': arg1, 'arg2': arg2, }