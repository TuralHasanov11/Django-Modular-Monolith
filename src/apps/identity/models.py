from __future__ import annotations

from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from enum import Enum
from django.db import models


class IdentityUserManager(UserManager):
    def get_default_queryset(self, *args, **kwargs) -> models.QuerySet[IdentityUser]:
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(superuser=False, is_staff=False)
        )


class Roles(Enum):
    ADMIN = "Admin", _("Admin")
    CUSTOMER = "Customer", _("Customer")


class IdentityUser(AbstractUser):
    email = models.EmailField(_("Email address"), unique=True)

    entities = IdentityUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
