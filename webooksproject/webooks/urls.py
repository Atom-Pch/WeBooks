from django.urls import path
from webooks.views import *

urlpatterns = [
    path("home/", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("books/search-results/", SearchView.as_view(), name="search"),
    path('books/search-results/genre=<int:genre_id>/', GenreSearchView.as_view(), name="search-genre"),
    path("books/book=<int:book_id>/", BookView.as_view(), name="book"),
]
