from django.urls import path, re_path

from finliveapp.api import auth_view, animal_view, feed_view, event_view, management_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = ([
    path(r'v1/auth/login', auth_view.Login.as_view(), name='login'),
    path(r'v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'v1/animal$', animal_view.Animals.as_view(), name='animals'),
    re_path(r'v1/animal/(?P<id>[0-9]+)$', animal_view.AnimalView.as_view(), name='animal'),
    re_path(r'v1/breed$', animal_view.BreedsView.as_view(), name='breeds'),
    re_path(r'v1/breed/(?P<id>[0-9]+)$', animal_view.BreedView.as_view(), name='breed'),
    re_path(r'v1/calving$', event_view.CalvingsView.as_view(), name='calvings'),
    re_path(r'v1/gender$', animal_view.GenderView.as_view(), name='gender'),
    re_path(r'v1/seedingtype$', animal_view.SeedingtypesView.as_view(), name='seedingtypes'),
    re_path(r'v1/seedingtype/(?P<id>[0-9]+)$', animal_view.SeedingtypeView.as_view(), name='seedingtype'),
    re_path(r'v1/feeding/feed$', feed_view.FeedsView.as_view(), name='feeds'),
    re_path(r'v1/feeding/feed/(?P<id>[0-9]+)$', feed_view.FeedView.as_view(), name='feed'),
    path(r'v1/feeding/feeding', feed_view.FeedingView.as_view(), name='feedings'),
    re_path(r'v1/management/barns$', management_view.BarnsView.as_view(), name='barns'),
    re_path(r'v1/management/barns/(?P<id>[0-9]+)$', management_view.BarnsView.as_view(), name='barn'),
    path(r'v1/management/equipments', management_view.EquipmentsView.as_view(), name='equipments'),
    re_path(r'v1/management/organizations$', management_view.OrganizationsView.as_view(), name='organizations'),
    re_path(r'v1/management/organizations/(?P<id>[0-9]+)$', management_view.OrganizationView.as_view(), name='organization'),
    path(r'v1/management/account', auth_view.Accounts.as_view(), name='accounts'),
    re_path(r'v1/management/account/(?P<id>[0-9]+)$', auth_view.Account.as_view(), name='account'),
], 'finliveapp')

