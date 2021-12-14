from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from finliveapp.decorators.access import check_user_organization, check_user_or_apikey
import pandas as pd
from finliveapp.models import GasMeasurement

class UploadView(APIView):
    @check_user_or_apikey()
    def post(self, request, *args, **kwargs):
        data = request.data
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        farmid = int(data.get('farmid'))
        filetype = data.get('type')
        if filetype == 'greenfeed':
            df = GasMeasurement.objects.read_greenfeed(data.get('file'))
            events = GasMeasurement.objects.create_measurements(df, organizationid, farmid)
            measurements = GasMeasurement.objects.bulk_create(events, batch_size=1000)
            return Response({}, status=status.HTTP_201_CREATED)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
