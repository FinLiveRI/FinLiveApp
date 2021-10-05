from django.core.validators import EMPTY_VALUES
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.utils.decorators import wraps

from finliveapp.models import AccountOrganization


def check_organization():

    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            organizationid = request.request.META.get('HTTP_X_ORG', None)
            account = request.request.user.useraccount
            if request.request.user.is_superuser:
                return func(request, *args, **kwargs)
            if isinstance(organizationid, int) or account not in EMPTY_VALUES:
                if AccountOrganization.objects.filter(account_id=account.id, organization_id=organizationid).exists():
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            else:
                return HttpResponseBadRequest()
        return wrapped
    return decorator





