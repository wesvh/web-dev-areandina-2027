from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView

from .forms import RegistrationForm


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("catalog:home")

    def get_success_url(self):
        requested_url = self.request.POST.get("next") or self.request.GET.get("next")
        if requested_url and url_has_allowed_host_and_scheme(
            requested_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return requested_url
        return str(self.success_url)


class FestivalLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class FestivalLogoutView(LogoutView):
    http_method_names = ["post", "options"]
    next_page = reverse_lazy("catalog:home")
