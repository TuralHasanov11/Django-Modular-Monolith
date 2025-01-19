from apps.main import views
from django.urls import path
from django.conf import settings

app_name = "apps.main"

urlpatterns = [
    path("", views.home, name="home"),
]


if settings.DEBUG:
    urlpatterns.append(path("protected/", views.protected, name="protected"))