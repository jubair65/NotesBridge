from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from .forms import RegisterForm


# Create your views here.
def home_view(request):
    return render(request,'home.html')


def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    return render(request,'accounts/register.html',{'form':form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
