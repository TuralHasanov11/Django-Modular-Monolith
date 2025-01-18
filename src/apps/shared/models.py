from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List


class LanguageField(models.CharField):
    description = _("Language field")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2
        kwargs["choices"] = settings.LANGUAGES
        kwargs["default"] = settings.LANGUAGE_CODE
        super().__init__(*args, **kwargs)


class CreatedAtField(models.DateTimeField):
    description = _("Created at field")

    def __init__(self, *args, **kwargs):
        kwargs["auto_now_add"] = True
        kwargs["editable"] = (False,)
        super().__init__(*args, **kwargs)


class UpdatedAtField(models.DateTimeField):
    description = _("Updated at field")

    def __init__(self, *args, **kwargs):
        kwargs["auto_now"] = True
        super().__init__(*args, **kwargs)
        
class DeletedAtField(models.DateTimeField):
    description = _("Deleted at field")

    def __init__(self, *args, **kwargs):
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


@dataclass
class DomainEventBase:
    occurred_at: datetime = datetime.now(timezone.utc)


class HasDomainEventsBase(models.Model):
    _domain_events: List[DomainEventBase] = []

    class Meta:
        abstract = True

    @property
    def domain_events(self):
        return self._domain_events

    def add_domain_event(self, domain_event: DomainEventBase) -> None:
        self._domain_events.append(domain_event)

    def remove_domain_event(self, domain_event: DomainEventBase) -> None:
        self._domain_events.remove(domain_event)

    def clear_domain_events(self) -> None:
        self._domain_events.clear()


class EntityBase(HasDomainEventsBase):
    class Meta:
        abstract = True


class AuditableEntity(models.Model):
    created_at = CreatedAtField()
    updated_at = UpdatedAtField()
    created_by_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    created_by_username = models.CharField(max_length=255, null=True, blank=True)
    updated_by_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    updated_by_username = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class SoftDeletableEntity(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = DeletedAtField()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    class Meta:
        abstract = True
