from django.urls import path, re_path

from finliveapp.api import auth_view, animal_view, management_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = ([
    path(r'v1/auth/login', auth_view.Login.as_view(), name='login'),
    path(r'v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'v1/auth/account', auth_view.Accounts.as_view(), name='accounts'),
    re_path(r'v1/auth/account/(?P<id>[0-9]+)$', auth_view.Account.as_view(), name='account'),
    re_path(r'v1/animal$', animal_view.Animals.as_view(), name='animals'),
    re_path(r'v1/animal/(?P<id>[0-9]+)$', animal_view.AnimalView.as_view(), name='animal'),
    re_path(r'v1/breed$', animal_view.BreedsView.as_view(), name='breeds'),
    re_path(r'v1/breed/(?P<id>[0-9]+)$', animal_view.BreedView.as_view(), name='breed'),
    re_path(r'v1/calving$', animal_view.CalvingsView.as_view(), name='calvings'),
    re_path(r'v1/gender$', animal_view.GenderView.as_view(), name='gender'),
    re_path(r'v1/management/barns$', management_view.BarnsView.as_view(), name='barns'),
    re_path(r'v1/management/barns/(?P<id>[0-9]+)$', management_view.BarnsView.as_view(), name='barn'),
    re_path(r'v1/management/organizations$', management_view.OrganizationsView.as_view(), name='organizations'),
    re_path(r'v1/management/organizations/(?P<id>[0-9]+)$', management_view.OrganizationView.as_view(), name='organization'),
], 'finliveapp')

