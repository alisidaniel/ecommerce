from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_hivKCJ0xUFTxuNUtDCjuvfh900NEVfvHmx")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_cgrGlYrWOyx9B3PiInCnscn1008VOdFn0B")
stripe.api_key = STRIPE_SECRET_KEY

from .models import BillingProfile, Card
def payment_method_view(request):
	next_url = None
	next_ 	 = request.GET.get('next')
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	if not billing_profile:
		return redirect("/cart")
	if is_safe_url(next_, request.get_host()):
		next_url = next_
	return render(request, "billing/payment-method.html", {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})

def payment_method_create_view(request):
	if request.method == "POST" and request.is_ajax():
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		if not billing_profile:
			return HttpResponse({"message": "Cannot find this user "}, status=401)
		token = request.POST.get("token")
		if token is not None:
			new_card_obj = Card.objects.add_new(billing_profile, token)
			print(new_card_obj)
		return JsonResponse({"message": "Your card was added."})
	return HttpResponse("error", status=401)