from django.urls import path

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostByCategory.as_view(), name='category'),
    path('cart/<str:slug>/', Cart_view.as_view(), name='cart'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add-new/', CartForm.as_view(), name='new'),
    path('edit/<slug:slug>/', cart_new_form, name='edit'),
    path('contact/', contact, name='contact'),
    path('search/', Search.as_view(), name='search'),
    # path('edit/<int:pk>/', cart_new_form, name='edit'),

]
