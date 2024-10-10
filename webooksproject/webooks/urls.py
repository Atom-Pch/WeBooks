from django.urls import path
from webooks.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("search-results/", SearchView.as_view(), name="search"),
    path('search-results/genre/<int:genre_id>/', GenreSearchView.as_view(), name="search-genre"),
]
