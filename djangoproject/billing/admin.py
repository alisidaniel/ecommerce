from django.contrib import admin
from .models import BillingProfile, Card, Charge
admin.site.register(BillingProfile)
admin.site.register(Charge)
admin.site.register(Card)
# Register your models here.
