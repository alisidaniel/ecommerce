from django.contrib.auth import authenticate, login, get_user_model 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from products.models import Product
from cart.models import Cart
# Create your views here.
def index(request):
	queryset = Product.objects.all()
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	context = {
	"cart": cart_obj,
    "product": queryset,
	}
	return render(request, 'posts/index.html', context)

def cart(request):
	return render(request, 'posts/cart.html')
def product_detail_page(request):
	return render(request, 'posts/product_details.html')
def product_page(request):
	return render(request, 'posts/product_page.html')
def invoice(request):
	return render(request, 'posts/invoice.html')