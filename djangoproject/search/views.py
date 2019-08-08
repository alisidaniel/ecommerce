from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
class SearchProductView(ListView):
	template_name =	"search/view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(SearchProductView, self).get_context_data(*args, **kwargs)
		query 	= self.request.GET.get('q')
		context['query'] = query
		return context
	def get_queryset(self, *args, **kwargs):
		request 	= self.request
		method_dict = request.GET
		query       = method_dict.get('q', None) # Method_dict['q']
		if query is not None:
			return Product.objects.search(query)
		if request.is_ajax():
			print("ajax request")
			ajax_result	= request.GET.get('data')
			jsondata = Product.objects.search(ajax_result)
			jsondata_serialize = serializers.serialize('json', jsondata)
			print(ajax_result)
			return JsonResponse(jsondata_serialize, safe=False)
		return Product.objects.featured()
		'''
		__icontains = field contains this
		__iexact = field is exactly this
		'''
