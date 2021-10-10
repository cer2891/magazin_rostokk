from django import template
from magazin_app.models import Cart, Tag

register = template.Library()


@register.inclusion_tag('magazin_app/popular_post_tpl.html')
def get_popular(cnt=5):
    carts = Cart.objects.order_by('-views')[:cnt]
    return {'carts': carts}


# @register.inclusion_tag('magazin_app/tag_tpl.html')
# def get_tags():
#     tags = Tag.objects.all()
#     return {'tags': tags}
