def get_client_ip(request):
	x_forward_for = request.META.get('HTTP_X_FORWARD_FOR')
	if x_forward_for:
		ip = x_forward_for.split(",")[0]
	else:
		ip = request.META.get("REMOTE_ADDR", None)
	return ip