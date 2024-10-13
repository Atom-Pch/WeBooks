import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from webooks.forms import *
from webooks.models import *
from django.db.models import Avg, Count

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()

        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('index')

        return render(request,'login.html', {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('index')

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()

        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')

        return render(request, 'register.html', {"form": form})

class IndexView(View):
    def get(self, request):
        newbooks = Book.objects.filter(
            status='approved',
            add_date__gte=datetime.date.today() - datetime.timedelta(days=30)
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            num_rating=Count('reviews')
        ).order_by('-add_date')[:10]

        bestbooks = Book.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            num_rating=Count('reviews')
        ).order_by('avg_rating')[:10]

        ourbooks = Book.objects.filter(author__name__startswith='Webooks').annotate(
            avg_rating=Avg('reviews__rating'),
            num_rating=Count('reviews')
        )

        context = {'newbooks': newbooks,
                   'bestbooks': bestbooks,
                   'ourbooks': ourbooks}

        return render(request, 'index.html', context)

class SearchView(View):
    def get(self, request):
        query = request.GET
        books = Book.objects.filter(title__icontains=query.get('search'))
        context = {'books': books,
                   'term': query.get('search')}

        return render(request, 'search.html', context)

class GenreSearchView(View):
    def get(self, request, genre_id):
        books = Book.objects.filter(genre__id=genre_id)
        genre = Genre.objects.get(id=genre_id)
        context = {'books': books,
                   'genre': genre}

        return render(request, 'search.html', context)

class BookView(View):
    def get(self, request, book_id):
        book = Book.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            num_rating=Count('reviews')
        ).get(id=book_id)
        context = {'book': book}

        return render(request, 'book.html', context)
    
    def post(self, request, book_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = Book.objects.get(id=book_id)
            review.user = UserProfile.objects.get(user=request.user)
            review.save()
            form.save_m2m()

            return redirect('book', book_id=book_id)

        return self.get(request, book_id)
