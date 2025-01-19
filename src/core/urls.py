from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("logs/", include("log_viewer.urls")),
]

urlpatterns += i18n_patterns(
    path("", include("apps.main.urls", namespace="main")),
    path("identity/", include("apps.identity.urls", namespace="identity")),
    path('accounts/', include('allauth.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r"^languages/", include("rosetta.urls")),
        path('api-auth/', include('rest_framework.urls'))
    ]
