# Generated by Django 5.1.3 on 2025-01-19 16:51

import apps.shared.models
import simple_history.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditablePost',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', apps.shared.models.DeletedAtField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('language', apps.shared.models.LanguageField(choices=[('en', 'English'), ('ru', 'Russian')], default='en', max_length=2)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical post',
                'verbose_name_plural': 'historical posts',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', apps.shared.models.CreatedAtField(auto_now_add=True)),
                ('updated_at', apps.shared.models.UpdatedAtField(auto_now=True)),
                ('created_by_username', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_by_username', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', apps.shared.models.DeletedAtField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('language', apps.shared.models.LanguageField(choices=[('en', 'English'), ('ru', 'Russian')], default='en', max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
