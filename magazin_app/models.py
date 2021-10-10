from django.db import models
# from django.template.defaultfilters import slugify
from django.urls import reverse
from pytils.translit import slugify


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title', ]


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Url_tag', unique=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['title', ]


class Cart(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    content = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликованно')
    price = models.IntegerField(verbose_name='Цена')
    number = models.IntegerField(verbose_name='Количество')
    photo_urll = models.URLField(verbose_name='Ссылка изображения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать ?')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True)
    views = models.IntegerField(default=0, verbose_name='Просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='cart',
                                 verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='carts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cart', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'
        ordering = ['created_at', ]
