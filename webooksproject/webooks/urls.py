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
    path("home/profile/", ProfileView.as_view(), name="profile"),
    path("home/book-requests/", BookRequestView.as_view(), name="book-request"),
    path("home/request-book/", RequestBookView.as_view(), name="request-book"),
    path("home/book-requests/approved-book=<int:book_id>/", BookApproveView.as_view(), name="approve-book"),
    path("home/book-requests/rejected-book=<int:book_id>/", BookRejectView.as_view(), name="reject-book"),
]
