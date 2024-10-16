import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from webooks.forms import *
from webooks.models import *
from django.db.models import Avg, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

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
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('index')

        return render(request, 'register.html', {"form": form})

class IndexView(View):
    def get(self, request):
        newbooks = Book.objects.filter(
            status='approved',
            add_date__gte=datetime.date.today() - datetime.timedelta(days=30)
        ).annotate(
            avg_rating=Avg('reviews__rating', filter=Q(reviews__status='ok')),
            num_rating=Count('reviews', filter=Q(reviews__status='ok'))
        ).order_by('-add_date')[:10]

        bestbooks = Book.objects.annotate(
            avg_rating=Avg('reviews__rating', filter=Q(reviews__status='ok')),
            num_rating=Count('reviews', filter=Q(reviews__status='ok'))
        ).filter(status='approved', avg_rating__gt=0).order_by('-avg_rating')[:10]

        context = {'newbooks': newbooks,
                   'bestbooks': bestbooks
                   }

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
                   'genre': genre
                   }

        return render(request, 'search.html', context)

class BookView(View):
    def get(self, request, book_id):
        book = Book.objects.annotate(
            avg_rating=Avg('reviews__rating', filter=Q(reviews__status='ok')),
            num_rating=Count('reviews', filter=Q(reviews__status='ok'))
        ).get(id=book_id)
        context = {'book': book,
                   'reviews': book.reviews.filter(status='ok').order_by('-reviewed_at'),
                   'genres': book.genre.order_by('name')
                   }

        return render(request, 'book.html', context)
    
class AddReviewView(View):
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

class ProfileView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login') 

        profile = UserProfile.objects.get(user=request.user)
        context = {'profile': profile}

        return render(request, 'profile.html', context)
    
class EditProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # Get the UserProfile of the currently authenticated user
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = EditProfileForm(instance=user_profile)

        return render(request, 'edit-profile.html', {'form': form})

    def post(self, request):
        # Get the UserProfile of the currently authenticated user
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = EditProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('profile')

        return render(request, 'edit-profile.html', {'form': form})

class BookRequestView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        books = Book.objects.filter(status='pending')

        return render(request, 'book-request.html', {'books': books})

class BookApproveView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        book = get_object_or_404(Book, id=book_id)
        form = ApproveBookForm(instance=book)
        authors = Author.objects.all().order_by('name')

        context = {'form': form, 'authors': authors}

        return render(request, 'approve-book.html', context)

    def post(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        book = get_object_or_404(Book, id=book_id)
        form = ApproveBookForm(data=request.POST, instance=book)
        if form.is_valid():
            form.save()

            return redirect('book-request')

        return render(request, 'approve-book.html', {'form': form})

class AuthorAddView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        form = AddAuthorForm()

        return render(request, 'add-author.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        form = AddAuthorForm(data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('add-author')

        return render(request, 'add-author.html', {'form': form})

class BookRejectView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        book = Book.objects.get(id=book_id)
        book.status = 'rejected'
        book.save()

        return redirect('book-request')

class HideReviewView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request, book_id, review_id):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        review = get_object_or_404(Review, id=review_id)
        review.status = 'hidden'
        review.save()

        return redirect('book', book_id=book_id)

class RequestBookView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = RequestBookForm()

        return render(request, 'request-book.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = RequestBookForm(data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('index')

        return render(request, 'request-book.html', {'form': form})

class AddShelfView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = AddShelfForm()

        return render(request, 'add-shelf.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = AddShelfForm(data=request.POST)
        if form.is_valid():
            shelf = form.save(commit=False)
            shelf.user = UserProfile.objects.get(user=request.user)
            shelf.save()
            form.save_m2m()

            return redirect('profile')

        return render(request, 'add-shelf.html', {'form': form})

class EditBookView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        book = get_object_or_404(Book, id=book_id)
        form = EditBookForm(instance=book)
        authors = Author.objects.all().order_by('name')

        context = {'form': form,
                   'authors': authors}

        return render(request, 'edit-book.html', context)

    def post(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        book = get_object_or_404(Book, id=book_id)
        form = EditBookForm(data=request.POST, instance=book)
        if form.is_valid():
            form.save()

            return redirect('book', book_id=book_id)

        return render(request, 'edit-book.html', {'form': form})
    
class RemoveBookView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        book = Book.objects.get(id=book_id)
        book.status = 'removed'
        book.save()

        return redirect('index')

class AddBookView(View, LoginRequiredMixin):
    login_url = 'login'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        authors = Author.objects.all().order_by('name')
        form = ApproveBookForm()

        context = {'form': form,
                   'authors': authors}

        return render(request, 'add-book.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('index')

        form = ApproveBookForm(data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('index')

        return render(request, 'add-book.html', {'form': form})