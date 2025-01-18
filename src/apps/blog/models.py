from __future__ import annotations
from django.db import models
from shared.models import AuditableEntity, SoftDeletableEntity, LanguageField


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def get_with_deleted(self):
        return super().get_queryset()


class Post(AuditableEntity, SoftDeletableEntity):
    title = models.CharField(max_length=255, null=False, blank=False)
    language = LanguageField()

    entities = PostManager()

    class Meta(AuditableEntity.Meta, SoftDeletableEntity.Meta):
        pass
