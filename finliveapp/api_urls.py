from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from finliveapp.api import auth_view, animal_view, animal_samples_view, feed_view, event_view, management_view,\
    charts_view, upload_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = ([
    path(r'v1/auth/login', auth_view.Login.as_view(), name='login'),
    path(r'v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'v1/auth/me', auth_view.Me.as_view(), name='me'),
    re_path(r'v1/animal$', animal_view.Animals.as_view(), name='animals'),
    re_path(r'v1/animal/(?P<id>[0-9]+)$', animal_view.AnimalView.as_view(), name='animal'),
    path(r'v1/bloodsample', animal_samples_view.BloodSamplesView.as_view(), name='bloodsamples'),
    re_path(r'v1/bloodsample/(?P<id>[0-9]+)$', animal_samples_view.BloodSampleView.as_view(), name='bloodsample'),
    re_path(r'v1/breed$', animal_view.BreedsView.as_view(), name='breeds'),
    re_path(r'v1/breed/(?P<id>[0-9]+)$', animal_view.BreedView.as_view(), name='breed'),
    re_path(r'v1/calving$', event_view.CalvingsView.as_view(), name='calvings'),
    path(r'v1/gasmeasurement', animal_samples_view.GasSystemsView.as_view(), name='gasmeasurements'),
    path(r'v1/gender', animal_view.GendersView.as_view(), name='genders'),
    re_path(r'v1/gender/(?P<id>[0-9]+)$', animal_view.GenderView.as_view(), name='gender'),
    path(r'v1/milking', event_view.MilkingEventsView.as_view(), name='milkings'),
    re_path(r'v1/milking/(?P<id>[0-9]+)$', event_view.MilkingEventView.as_view(), name='milking'),
    re_path(r'v1/seedingtype$', animal_view.SeedingtypesView.as_view(), name='seedingtypes'),
    re_path(r'v1/seedingtype/(?P<id>[0-9]+)$', animal_view.SeedingtypeView.as_view(), name='seedingtype'),
    path(r'v1/weighting', event_view.WeightingsView.as_view(), name='weightings'),
    path(r'v1/charts/feedingduration', charts_view.FeedingDuration.as_view(), name='feedingduration'),
    path(r'v1/charts/animalchart', charts_view.AnimalChartsView.as_view(), name='animalchartsview'),
    path(r'v1/charts/downloadanimalchart', charts_view.AnimalChart.as_view(), name='downloadanimalchart'),
    re_path(r'v1/feeding/feed$', feed_view.FeedsView.as_view(), name='feeds'),
    re_path(r'v1/feeding/feed/(?P<id>[0-9]+)$', feed_view.FeedView.as_view(), name='feed'),
    path(r'v1/feeding/feeding', feed_view.FeedingView.as_view(), name='feedings'),
    re_path(r'v1/feeding/feeding/(?P<id>[0-9]+)$', feed_view.FeedingSingleView.as_view(), name='singlefeeding'),
    re_path(r'v1/management/barns$', management_view.BarnsView.as_view(), name='barns'),
    re_path(r'v1/management/barns/(?P<id>[0-9]+)$', management_view.BarnsView.as_view(), name='barn'),
    path(r'v1/management/equipments', management_view.EquipmentsView.as_view(), name='equipments'),
    re_path(r'v1/management/organizations$', management_view.OrganizationsView.as_view(), name='organizations'),
    re_path(r'v1/management/organizations/(?P<id>[0-9]+)$', management_view.OrganizationView.as_view(), name='organization'),
    path(r'v1/management/account', auth_view.Accounts.as_view(), name='accounts'),
    re_path(r'v1/management/account/(?P<id>[0-9]+)$', auth_view.Account.as_view(), name='account'),
    re_path(r'v1/upload', upload_view.UploadView.as_view(), name='upload'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT), 'finliveapp')

