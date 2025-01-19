from __future__ import annotations

from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from enum import Enum
from django.db import models

class Groups(Enum):
    ADMIN = "Admin", _("Admin")
    CUSTOMER = "Customer", _("Customer")


class User(AbstractUser):
    email = models.EmailField(_("Email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
