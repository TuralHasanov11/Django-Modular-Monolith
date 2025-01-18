from django.urls import path
from apps.identity import views as identity_views


app_name = "identity"

urlpatterns = [
    path("login", identity_views.LoginView.as_view(), name="login"),
    path(
        "register",
        identity_views.RegistrationView.as_view(),
        name="register",
    ),
    path("logout", identity_views.LogoutView.as_view(), name="logout"),
    path("lockout", identity_views.lockout, name="lockout"),
]
