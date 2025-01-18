from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class LoginForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-3 form-control-sm",
                "placeholder": "Email",
                "title": _("Please enter email"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Password",
                "title": _("Please enter password"),
            }
        ),
    )

    def confirm_login_allowed(self, user):
        pass


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label=_('Username'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Username'), 'title': _('Please enter username')}))
    first_name = forms.CharField(label=_('First Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('First Name'), 'title': _('Please enter first name')}))
    last_name = forms.CharField(label=_('Last Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Last Name'), 'title': _('Please enter last name')}))
    email = forms.EmailField(label=_('Email'), max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Email'), 'title': _('Please enter email')}))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Password'), 'title': _('Please enter password')}))
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Password Confirm'), 'title': _('Please confirm password')}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email