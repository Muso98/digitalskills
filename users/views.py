from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ContactForm
from django.db.models import F, Sum, ExpressionWrapper, DurationField
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
def index(request):
    return render(request, 'index.html')


def home_redirect(request):
    """
    Foydalanuvchini asosiy sahifaga yo'naltirish.
    """
    return redirect('users:home')

# Login sahifasi
def login_view(request):
    """
    Foydalanuvchi tizimga kirishi.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Muvaffaqiyatli kirish
        return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Logout sahifasi
def logout_view(request):
    """
    Foydalanuvchini tizimdan chiqarish.
    """
    logout(request)
    messages.success(request, _("Siz tizimdan muvaffaqiyatli chiqdingiz."))
    return redirect('login')


# Ro'yxatdan o'tish sahifasi


def signup_view(request):
    """
    Foydalanuvchini ro'yxatdan o'tkazish.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')  # Ro'yxatdan o'tgandan so'ng login sahifasiga yo'naltirish
    else:
        form = SignUpForm()
    return render(request, 'registration/sign-up.html', {'form': form})


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/forget-password.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = _("Parolni tiklash havolasi elektron pochtangizga yuborildi.")
    success_url = '/users/login/'

forget_password_view = CustomPasswordResetView.as_view()
# About sahifasi
def about(request):
    """
    Platforma haqida ma'lumot sahifasi.
    """
    return render(request, 'about.html')

# Aloqa sahifasi (Contact Page)

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Ma'lumotlarni saqlash
            messages.success(request, _("So‘rovingiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog‘lanamiz."))
            return redirect('users:contact')  # Forma yuborilgandan keyin qaytish
    else:
        form = ContactForm()

    return render(request, 'help-center-support.html', {'form': form})