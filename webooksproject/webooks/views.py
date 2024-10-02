from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('home')

        return render(request,'login.html', {"form":form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
