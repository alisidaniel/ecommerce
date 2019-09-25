from django.conf import settings
from django.shortcuts import render, redirect
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile
from .models import Cart
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

from addresses.forms import AddressForm
from addresses.models import Address
from django.http import JsonResponse

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_hivKCJ0xUFTxuNUtDCjuvfh900NEVfvHmx")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_cgrGlYrWOyx9B3PiInCnscn1008VOdFn0B")
stripe.api_key = STRIPE_SECRET_KEY
# Create your views here.
def cart_detail_api_view(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	products = [{
			"id":x.id,
			"url":x.get_absolute_url(),
			"name": x.title, 
			"price": x.price,
			"quantity":x.quantity,} 
	for x in cart_obj.products.all()]
	cart_data = {"products": products, "subtotal":cart_obj.subtotal, "total":cart_obj.total}
	return JsonResponse(cart_data)

def cart(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	return render(request, "cart/cart.html", {"cart": cart_obj})

def cart_update(request):
	product_id = request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist :
			return redirect("cart:view")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			request.session['cart_items'] = cart_obj.products.count()
			added = False
		else:
			print("added to cart")
			cart_obj.products.add(product_obj)
			request.session['cart_items'] = cart_obj.products.count()
			added = True
		if request.is_ajax():
			json_data = {
				"added": added,
				"removed": not added,
				"cartItemCount": cart_obj.products.count()
			}
			return JsonResponse(json_data)
	return redirect("cart:view")

def Checkout(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_created or cart_obj.products.count() == 0:
		return redirect("cart:view")	
		
	login_form = LoginForm()
	guest_form = GuestForm()
	address_form = AddressForm()
	billing_address_id = request.session.get("billing_address_id", None)
	shipping_address_id = request.session.get("shipping_address_id", None)
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	address_qs = None
	has_card = False
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if shipping_address_id or billing_address_id:
			order_obj.save()
		has_card = billing_profile.has_card
# Cart checkout finalize or done
	if request.method == "POST":
		is_prepared = order_obj.check_done()
		if is_prepared:
			did_charge, crg_msg = billing_profile.charge(order_obj)
			if did_charge:
				order_obj.mark_paid()
				request.session['cart_items'] = 0
				del request.session['cart_id']
				if not billing_profile.user:
					billing_profile.set_cards_inactive()
				return redirect("cart:success")
			else:
				print(crg_msg)
				return redirect("cart:checkout")

	context = {
		"object": order_obj,
		"billing_profile": billing_profile,
		"login_form": login_form,
		"guest_form": guest_form,
		"address_form": address_form,
		"address_qs": address_qs,
		"has_card": has_card,
		"publish_key": STRIPE_PUB_KEY,
		}
	return render(request, "cart/checkout.html", context)

def checkout_done_view(request):
	return render(request, "cart/checkout-done.html", {})

def invoice(request):
	return render(request, "cart/invoice.html", {})