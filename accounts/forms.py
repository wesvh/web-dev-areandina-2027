from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    """Public registration form using Django's built-in user and validators."""
