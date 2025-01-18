from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView
from django.contrib.auth import views as auth_views
from apps.identity.models import IdentityUser
from apps.identity.forms import LoginForm, RegistrationForm


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    redirect_field_name = reverse_lazy("main:home")
    redirect_authenticated_user = True
    template_name = 'identity/login.html'
    
class RegistrationView(CreateView):
    form_class = RegistrationForm
    redirect_field_name = reverse_lazy("main:home")
    redirect_authenticated_user = True
    template_name = 'identity/register.html'
    model = IdentityUser
    success_url = reverse_lazy('identity:login')
    

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy('main:home')