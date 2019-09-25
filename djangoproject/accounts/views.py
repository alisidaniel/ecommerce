from django.contrib.auth import authenticate, login, get_user_model 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, DetailView	
from django.utils.http import is_safe_url
from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
from .signals import user_logged_in

# Create your views here.
@login_required
def account_home_view(request):
	return render(request, "views/home.html", {})
#  
class AccountHomeView(LoginRequiredMixin, DetailView):
	template_name = 'views/home.html'
	def get_object(self):
		return self.request.user

def guest_register_view(request):
	form = GuestForm(request.POST or None) 
	context={"form" : form}
	next_ 			= request.GET.get('next')
	next_post 		= request.POST.get('next')
	redirect_path	= next_ or next_post or None
	if form.is_valid():
		email = form.cleaned_data.get("email")
		new_guest_email = GuestEmail.objects.create(email=email)
		request.session['guest_email_id'] = new_guest_email.id
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		else:
			return redirect("/register/")
	return redirect("/register/")

class LoginView(FormView):
	form_class = LoginForm
	template_name = 'views/login.html'
	success_url = '/'
	def form_valid(self, form):
		request = self.request
		next_ 			= request.GET.get('next')
		next_post 		= request.POST.get('next')
		redirect_path	= next_ or next_post or None
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user)
			user_logged_in.send(user.__class__, instance=user, request=request)
			try:
				del request.session['guest_email_id']
			except:
				pass 
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("/")
		return super(LoginView, self).form_invalid(form)

class RegisterView(CreateView):
	form_class = RegisterForm
	template_name =	'views/register.html'
	success_url = '/login/'

# def login_page(request):
# 	form = LoginForm(request.POST or None)
# 	context={"form" : form}
# 	next_ 			= request.GET.get('next')
# 	next_post 		= request.POST.get('next')
# 	redirect_path	= next_ or next_post or None
# 	if form.is_valid():
# 		username = User.objects.get(email=form.cleaned_data['email'])
# 		password = form.cleaned_data.get("password")
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			login(request, user)
# 			try:
# 				del request.session['guest_email_id']
# 			except:
# 				pass 
# 			if is_safe_url(redirect_path, request.get_host()):
# 				return redirect(redirect_path)
# 			else:
# 				return redirect("/")
# 		else:
# 			print('failed logged in')
# 			return redirect("/")

# 	return render(request, 'views/login.html', context)

# User = get_user_model()
# def register_page(request):
# 	form = RegisterForm(request.POST or None)
# 	context={
# 	"form" : form,
# 	}
# 	if form.is_valid():
# 		form.save()
# 	return render(request, 'views/register.html', context)