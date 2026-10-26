from django.urls import path

from .views import FestivalLoginView, FestivalLogoutView, RegistrationView


app_name = "accounts"

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", FestivalLoginView.as_view(), name="login"),
    path("logout/", FestivalLogoutView.as_view(), name="logout"),
]
