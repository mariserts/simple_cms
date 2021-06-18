from rest_framework import permissions

from .models import Thing


class AuthenticatedUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_authenticated is False:
            return False

        if request.user.is_superuser is True:
            return True

        # codename = request.resolver_match.kwargs.get('codename', None)
        tenant_id = request.resolver_match.kwargs.get('tenant_id', None)

        if tenant_id is None:
            return True

        # if codename is None:
        #     return TenantUser.objects.filter(
        #         tenant_id=tenant_id,
        #         user_id=request.user.id
        #     )
        # else:
        #     pass

        return TenantUser.objects.filter(
            tenant_id=tenant_id,
            user_id=request.user.id
        ).exists()
