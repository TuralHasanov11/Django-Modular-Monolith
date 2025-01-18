from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from apps.identity import views as identity_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("logs/", include("log_viewer.urls")),
]

urlpatterns += i18n_patterns(
    path("", include("apps.main.urls", namespace="main")),
    path("", include("apps.inventory.urls", namespace="inventory")),
    path("", include("apps.store.urls", namespace="store")),
    path("identity/", include("apps.identity.urls", namespace="identity")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r"^languages/", include("rosetta.urls")),
        path('api-auth/', include('rest_framework.urls'))
    ]
