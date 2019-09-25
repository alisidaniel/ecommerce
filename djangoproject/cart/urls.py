from django.conf.urls import url
from .views import (cart, cart_update, Checkout, checkout_done_view, invoice
	)
urlpatterns = [
	url(r'^$', cart, name="view"),
	url(r'^checkout/$', Checkout, name="checkout"),
	url(r'^checkout/success/$', checkout_done_view, name="success"),
	url(r'^update/$', cart_update, name="update"),
	url(r'^invoice/$', invoice, name="invoice"),
]