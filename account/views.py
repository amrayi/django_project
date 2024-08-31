from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from config import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .models import User, VerificationCode
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin, AuthorAccessMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.models import Article

# Create your views here.
class ArticleList(AuthorAccessMixin, ListView):
    template_name = "registration/home.html"
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author = self.request.user)
        
class ArticleCreate(AuthorAccessMixin, FormValidMixin ,FieldsMixin, CreateView):
    model = Article
    template_name = "registration/article_create_update.html"
    
class ArticleUpdate(AuthorAccessMixin, FormValidMixin ,FieldsMixin, UpdateView):
    model = Article
    template_name = "registration/article_create_update.html"
    
class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_confirm_delete.html'
    
class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "registration/profile.html"
    fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'special_user', 'is_auther']
    success_url = reverse_lazy('account:profile')
    
    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)
    
    def get_forms_kwargs(self):
        kwargs = super(Profile, self).get_forms_kwargs()
        kwargs.update({
            'user' : self.request.user
        })
        return kwargs
    
class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        
        if user.is_superuser or user.is_auther:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')
        
class Logout(LogoutView):
    def get(self, request):
        logout(request)
        # return HttpResponseRedirect(settings.LOGIN_URL)
        return reverse_lazy('account:logout')


from django.http import HttpResponse
from .forms import SignupForm
from django.template.loader import render_to_string
from account.models import User
from zeep import Client
from django.shortcuts import render, redirect
from .utils import send_sms
import random

# class Register(CreateView):
#     form_class = SignupForm
#     template_name = "registration/register.html"
    
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
        
#         send_verification_code()
        
#         # uid = urlsafe_base64_decode(force_bytes(user.pk))
#         # token = account_activation_token.make_token(user)

# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         # return redirect('home')
#         return HttpResponse('اکانت شما با موفقیت فعال شد. برای ورود <a href="/login">کلیک<a> کنید.')
#     else:
#         return HttpResponse('لینک فعال سازی منقضی شده است. <a href="/registration">دوباره امتحان کنید.<a>')
    
USERNAME = 'realamra'
PASSWORD = 'Amir@1234'

def send_verification_code(phone_number, code):
    client = Client('https://api.payamak-panel.com/post/Send.asmx?wsdl')
    client.service.SendSimpleSMS2(
        Username=USERNAME,
        Password=PASSWORD,
        MobileNumber=phone_number,
        Message=f'کد تایید شما: {code}',
        LineNumber='09190027944'
    )

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            verification_code = random.randint(100000, 999999)
            
            request.session['phone_number'] = phone_number
            request.session['verification_code'] = verification_code
            send_verification_code(phone_number, verification_code)
            
            return redirect('verify')
    else:
        form = SignupForm()
    
    return render(request, 'registration/register.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        verification_code = request.session.get('verification_code')
        
        if entered_code == str(verification_code):
            phone_number = request.session.get('phone_number')
            
            return HttpResponse('اکانت شما با موفقیت فعال شد. برای ورود <a href="/login">کلیک<a> کنید.')
        else:
            return HttpResponse('لینک فعال سازی منقضی شده است. <a href="/registration">دوباره امتحان کنید.<a>')
    
    return render(request, 'registration/register_confirm.html')

