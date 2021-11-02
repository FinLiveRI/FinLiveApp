from django.core.validators import EMPTY_VALUES
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.utils.decorators import wraps

from finliveapp.models import AccountOrganization, OrganizationAPIKey


def check_user_organization():

    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            if request.request.user.is_anonymous:
                return HttpResponseForbidden()
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


def check_user_or_apikey():

    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            organizationid = request.request.META.get('HTTP_X_ORG', None)
            if organizationid in EMPTY_VALUES:
                return HttpResponseBadRequest()
            if request.request.user.is_superuser:
                return func(request, *args, **kwargs)
            if request.request.user.is_anonymous:
                key = request.request.META["HTTP_AUTHORIZATION"].split()[1]
                api_key = OrganizationAPIKey.objects.get_from_key(key)
                if api_key not in EMPTY_VALUES and api_key.organization_id == int(organizationid):
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            account = request.request.user.useraccount
            if isinstance(organizationid, int) or account not in EMPTY_VALUES:
                if AccountOrganization.objects.filter(account_id=account.id, organization_id=organizationid).exists():
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            else:
                return HttpResponseBadRequest()
        return wrapped
    return decorator



