from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
from typing import Type
from abc import abstractmethod, ABC
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from apps.identity.models import IdentityUser
from django.dispatch import receiver
from simple_history.signals import post_create_historical_record
from typing import Protocol


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


class AggregateRoot(Protocol):
    pass


@dataclass
class DomainEventBase:
    occurred_at: datetime = datetime.now(timezone.utc)


class HasDomainEvents(Protocol):
    _domain_events: List[DomainEventBase]

    def add_domain_event(self, domain_event: DomainEventBase) -> None:
        ...

    def remove_domain_event(self, domain_event: DomainEventBase) -> None:
        ...

    def clear_domain_events(self) -> None:
        ...

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
    class Meta:  # type: ignore
        abstract = True


class AuditRecords(HistoricalRecords):
    def __init__(self, *args, **kwargs):
        kwargs["inherit"] = True
        kwargs["custom_model_name"] = lambda x: f"Auditable{x}"
        super().__init__(*args, **kwargs)


class AuditableEntity(EntityBase):
    created_at = CreatedAtField()
    updated_at = UpdatedAtField()
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    created_by_username = models.CharField(max_length=255, null=True, blank=True)
    updated_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    updated_by_username = models.CharField(max_length=255, null=True, blank=True)
    history = AuditRecords(
        excluded_fields=[
            "created_at",
            "updated_at",
            "created_by_user",
            "created_by_username",
            "updated_by_user",
            "updated_by_username",
        ]
    )

    class Meta:  # type: ignore
        abstract = True


class SoftDeletable(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = DeletedAtField()
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)


@receiver(post_create_historical_record)
def post_create_historical_record_callback(
    sender: Type[AuditableEntity],
    instance: AuditableEntity,
    history_user: IdentityUser,
    **kwargs,
):
    if instance.created_by_user is None:
        instance.__class__.objects.filter(pk=instance.pk).update(
            created_by_user=history_user,
            created_by_username=history_user.username,
            updated_by_user=history_user,
            updated_by_username=history_user.username,
        )
    else:
        print("Updating updated_by_user")
        sender.objects.filter(pk=instance.pk).update(
            updated_by_user=history_user, updated_by_username=history_user.username
        )
