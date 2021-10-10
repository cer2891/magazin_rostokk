from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
# from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Cart, Category


# class NewsAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = News
#         fields = '__all__'


class CartAdmin(admin.ModelAdmin):
    # form = Cart
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'category', 'number', 'price', 'views', 'is_published',)
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'views',)
    list_filter = ('category',)
    fields = ('title', 'slug', 'category', 'content', 'photo', 'photo_urll',
              'views', 'price', 'number', 'created_at',)
    readonly_fields = ('views', 'created_at',)
    save_on_top = True
    save_as = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Cart, CartAdmin)
admin.site.register(Category, CategoryAdmin)
