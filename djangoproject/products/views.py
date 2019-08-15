from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from analytics.mixins import ObjectViewedMixin
from .models import Product
from cart.models import Cart

# Create your views here.
# def product_details(request, pk=None, *args, **kwargs):
# 	if pk:
# 		instance = get_object_or_404(Product, pk=pk)
# 	else:
# 		raise Http404("Product doesn't exist")
# 	context  = {
# 	'object' : instance
# 	}
# 	return render(request, "products/product_details.html", context)

class ProductFeaturedListView(ListView):
	template_name = "products/list.html"
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.featured()

class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
	template_name = "products/featured-details.html"
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.featured()

class product_view(ListView):
	queryset = Product.objects.all()
	template_name = "products/product_page.html"
	
	def get_context_data(self, *args, **kwargs):
		context  = super(product_view, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

class product_view_slug(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all()
	template_name = "products/product_details.html"

	def get_context_data(self, *args, **kwargs):
		context  = super(product_view_slug, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_object(self, *args, **kwargs):
		request =self.request
		slug = self.kwargs.get('slug')
		#instance = get_object_or_404(Product, slug=slug, active=True)
		try:
			instance = Product.objects.get(slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404(" Not found..")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True)
			instance =qs.first()
		except:
			raise Http404(" Big Problem")
		#object_viewed_signal.send(instance.__class__, instance=instance, request=request)
		return instance

class cart(ListView):
	template_name = "products/cart.html"

class invoice(ListView):
	template_name = "products/invoice.html"