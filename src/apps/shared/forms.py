from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class LanguageField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs["label"] = _("Language")
        kwargs["choices"] = settings.LANGUAGES
        kwargs["widget"] = forms.Select(
            attrs={
                "class": "form-select form-select-sm",
                "readonly": True,
                "title": _("Please select language"),
            }
        )
        super().__init__(*args, **kwargs)
