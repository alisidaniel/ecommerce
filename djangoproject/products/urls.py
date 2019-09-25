from django.conf.urls import url
from .views import (invoice, product_view, cart, product_view_slug, category_slug_view
	)
urlpatterns = [
	url(r'^$', product_view.as_view()),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', category_slug_view.as_view(), name='categories_display'),
	url(r'^(?P<slug>[\w-]+)/$', product_view_slug.as_view()),
]