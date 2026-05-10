from django.shortcuts import render
from django.contrib.auth import logout,login
from .models import Users
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect


def users_list(request):
    users = Users.objects.all()
    return render(request, 'users.html', {'users': users})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # or wherever you want to redirect
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and password:
            user = Users.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')  # Redirect to login page after signup
    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    return redirect('login')