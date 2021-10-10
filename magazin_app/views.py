# from urllib import request

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F
from django.urls import reverse_lazy
from .models import Cart, Category
from .forms import UserLoginForm, NewForm


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'magazin_app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def contact(request):
    title = 'Контакты'
    return render(request, 'magazin_app/contact.html', {'title': title})


class Cart_view(DetailView):
    model = Cart
    template_name = 'magazin_app/single.html'
    context_object_name = 'cart'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['title'] = Cart.objects.get(slug=self.kwargs['slug'])
        return context


class Home(ListView):
    model = Cart
    template_name = 'magazin_app/index.html'
    context_object_name = 'carts'
    paginate_by = 6

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         queryset = Cart.objects.filter(is_published=True).select_related('category')
    #     else:
    #         queryset = Cart.objects.select_related('category')
    #
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Семена'
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related("category")
        if not self.request.user.is_authenticated:
            return Cart.objects.filter(is_published=True).select_related('category').order_by('title')
        else:
            return Cart.objects.select_related('category').order_by('title')


class PostByCategory(ListView):
    template_name = 'magazin_app/index.html'
    context_object_name = 'carts'
    paginate_by = 6
    allow_empty = False

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Cart.objects.filter(category__slug=self.kwargs['slug'], is_published=True).select_related('category').order_by('title')
        else:
            return Cart.objects.filter(category__slug=self.kwargs['slug']).select_related('category').order_by('title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class Search(ListView):
    template_name = 'magazin_app/search.html'
    context_object_name = 'carts'
    # paginate_by = 1

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Cart.objects.filter(is_published=True, title__icontains=self.request.GET.get('s'))
        else:
            return Cart.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CartForm(CreateView):
    form_class = NewForm
    template_name = 'magazin_app/add_news.html'
    # success_url = reverse_lazy('home')
    queryset = Cart.objects.select_related('category')
    # login_url = '/admin/'
    raise_exception = True

    # def get_success_url(self):
    #     return reverse_lazy('cart', kwargs={'slug': self.get('slug')})


# class CartNewForm(CreateView):
#     form_class = NewForm()
#     cart = Cart.objects.get(pk=1)
#     form_class = NewForm(instance=cart)
#     template_name = 'magazin_app/add_news.html'
#     success_url = reverse_lazy('home')
#     queryset = Cart.objects.select_related('category')
#     # login_url = '/admin/'
#     raise_exception = True


def cart_new_form(request, slug):
    # print(slug)
    cartt = get_object_or_404(Cart, slug=slug)
    if request.method == 'POST':
        form = NewForm(request.POST, instance=cartt)
        if form.is_valid():
            cart = form.save()
            return redirect(cart)
    else:
        form = NewForm(instance=cartt)
    return render(request, 'magazin_app/edit.html',
                  {'form': form, 'cart': cartt})
