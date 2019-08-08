from django.conf.urls import url
from .views import (invoice, product_view, cart, product_view_slug
	)
urlpatterns = [
	url(r'^$', product_view.as_view()),
	url(r'^(?P<slug>[\w-]+)/$', product_view_slug.as_view()),
]