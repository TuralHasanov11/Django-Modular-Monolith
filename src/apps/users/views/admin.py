from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView

from apps.identity.models import User


# class UserListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
#     model = IdentityUser
#     template_name = "users/admin/list.html"
#     context_object_name = "users"
#     permission_required = ["users.view_user"]

#     def get_queryset(self):
#         return IdentityUser.entities.get_default_queryset().only(
#             "username", "email", "date_joined"
#         )


# class UserCreateView(
#     LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
# ):
#     model = IdentityUser
#     form_class = forms.UserCreateForm
#     template_name = "users/admin/create.html"
#     success_message = _("User was created successfully!")
#     success_url = reverse_lazy("apps.administration:user-list")
#     permission_required = ["users.add_user"]


# class UserDeleteView(
#     LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView
# ):
#     model = IdentityUser
#     success_message = _("User was deleted successfully!")
#     success_url = reverse_lazy("apps.users:admin-user-list")
#     permission_required = ["users.delete_user"]

#     def get_queryset(self, *args, **kwargs):
#         return IdentityUser.entities.get_default_queryset(*args, **kwargs)
