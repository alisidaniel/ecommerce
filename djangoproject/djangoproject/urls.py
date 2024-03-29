"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from accounts.views import LoginView, RegisterView, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from cart.views import cart_detail_api_view   
urlpatterns = [
    url(r'^$', include('posts.urls')),
    path('index/', include('posts.urls')),
    url(r'^login/', LoginView.as_view(), name='login'),
     url(r'^register/guest', guest_register_view, name='guest_register'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^products/', include("products.urls")),
    url(r'^api/cart/', cart_detail_api_view, name='api-cart'),
    url(r'^cart/', include(("cart.urls", 'cart'), namespace='cart')),
    url(r'^search/', include(("search.urls", 'search'), namespace='search')),
    url(r'^checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('admin/', admin.site.urls),   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)