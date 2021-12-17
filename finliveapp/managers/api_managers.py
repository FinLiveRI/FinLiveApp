from django.db import models
from django.db.models import F
import pandas as pd

"""QuerySet for managing API queries"""
class ApiQuerySet(models.QuerySet):

    """Get nice names for api values """
    def _get_api_fields(self):
        annotations = {}
        new_fields = []
        for f in self.model.Api.fields:
            if '__' in f:
                table, name = f.split('__')
                if table == "barn":
                    n = name
                else:
                    #n = table + name
                    n = table.upper()
                #n = [1]
                # Check for duplicate values
                #if n in new_fields:
                #    n = f.replace('__', '_')
                annotations[n] = F(f)
                new_fields.append(n)
            else:
                new_fields.append(f)
        return new_fields, annotations

    def api_values(self):
        fields, annotations = self._get_api_fields()
        return self.values(*fields, **annotations)

    def to_dataframe(self):
        fields, annotations = self._get_api_fields()
        qs = self.values(*fields, **annotations)
        return pd.DataFrame.from_records(list(qs), columns=fields, coerce_float=True)

"""Model manager for managing API queries"""
class ApiManager(models.Manager):

    def get_queryset(self):
        return ApiQuerySet(self.model)

    def to_dataframe(self):
        return self.get_queryset().to_dataframe()

