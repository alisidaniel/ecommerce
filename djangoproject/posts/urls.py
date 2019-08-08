from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product_detail/', views.cart, name='product_detail'),
    url(r'^product_page/', views.cart, name='product_page'),
]; 