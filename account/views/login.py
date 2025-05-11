from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Foydalanuvchi nomi yoki parol noto‘g‘ri!')
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki parol noto‘g‘ri!')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz!')
    return redirect('login')
