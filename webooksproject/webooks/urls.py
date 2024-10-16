from django.urls import path
from webooks.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("home/", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("books/search-results/", SearchView.as_view(), name="search"),
    path('books/search-results/genre/<int:genre_id>/', GenreSearchView.as_view(), name="search-genre"),
    path("books/book/<int:book_id>/", BookView.as_view(), name="book"),
    path("books/book/add-review/<int:book_id>/", AddReviewView.as_view(), name="add-review"),
    path("home/profile/", ProfileView.as_view(), name="profile"),
    path("home/profile/change-password/", auth_views.PasswordChangeView.as_view(template_name='change-password.html'), name="change-password"),
    path("home/profile/change-password/done/", auth_views.PasswordChangeDoneView.as_view(template_name='change-password-done.html'), name="password_change_done"),
    path("home/book-requests/", BookRequestView.as_view(), name="book-request"),
    path("home/request-book/", RequestBookView.as_view(), name="request-book"),
    path("home/book-requests/approve-book/<int:book_id>/", BookApproveView.as_view(), name="approve-book"),
    path("home/book/add-author/", AuthorAddView.as_view(), name="add-author"),
    path("home/book-requests/reject-book/<int:book_id>/", BookRejectView.as_view(), name="reject-book"),
    path("home/profile/edit/", EditProfileView.as_view(), name="edit-profile"),
    path("books/book/review/<int:book_id>/hide-review/<int:review_id>/", HideReviewView.as_view(), name="hide-review"),
]
