import datetime
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from webooks.forms import RegisterForm
from webooks.models import *
from django.db.models import Avg

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()

        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('home')

        return render(request,'login.html', {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('home')

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()

        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

        return render(request, 'register.html', {"form": form})

class HomeView(View):
    def get(self, request):
        newbooks = Book.objects.filter(
            status='approved',
            add_date__gte=datetime.date.today() - datetime.timedelta(days=30)
        ).order_by('-add_date')[:10]

        bestbooks = Book.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating')[:10]

        ourbooks = Book.objects.filter(author__name__startswith='Webooks')

        context = {
            'newbooks': newbooks,
            'bestbooks': bestbooks,
            'ourbooks': ourbooks
        }

        return render(request, 'home.html', context)

class SearchView(View):
    def get(self, request):
        query = request.GET
        books = Book.objects.filter(title__icontains=query.get('search'))
        context = {'books': books,
                   'term' : query.get('search')}

        return render(request, 'search.html', context)

class GenreSearchView(View):
    def get(self, request, genre_id):
        if genre_id:
            books = Book.objects.filter(genre__id=genre_id)
            genre = Genre.objects.get(id=genre_id)

        context = {
            'books': books,
            'genre': genre
        }
        return render(request, 'search.html', context)
