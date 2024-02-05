from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

from django.urls import reverse_lazy


class UpdatedRequiredMixin(PermissionRequiredMixin):
    """
    """
    def has_permission(self):
        user = self.request.user
        if not user.is_authenticated:
            return False

        if user.type_updated:
            return True
        return False

    def handle_no_permission(self):
       
        # return redirect('apps.core.profile-update')
        return redirect(reverse_lazy('apps.core:profile-update'))
        # return redirect('<uuid:pk>/update/')