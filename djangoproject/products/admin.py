from django.contrib import admin
from .models import  Product, Category, Manufacturer
class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']
	class Meta:
		model = Product
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Manufacturer)
# Register your models here.
