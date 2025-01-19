from __future__ import annotations
from django.db import models
from apps.shared.models import (
    AuditableEntity,
    DeletedAtField,
    AuditRecords,
    LanguageField,
    SoftDeletable,
)
from datetime import datetime, timezone


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def get_with_deleted(self):
        return super().get_queryset()


class Post(AuditableEntity, SoftDeletable):
    title = models.CharField(max_length=255, null=False, blank=False)
    language = LanguageField()

    objects = PostManager()

    class Meta(AuditableEntity.Meta, SoftDeletable.Meta):
        pass
