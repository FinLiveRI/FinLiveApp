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
                if table in ["breed", "organization"]:
                    n = table.upper()
                    #print(n)
                else:
                    #n = '{0}_{1}'.format(table, name)
                    n = name
                # Check for duplicate values
                #if n in new_fields:
                #    n = f.replace('__', '_')
                annotations[n] = F(f)
                new_fields.append(n)
            else:
                new_fields.append(f)
        return new_fields, annotations

    def _lower_keys(self, d):
        return {k.lower(): v for k, v in d.items()}

    def api_values(self):
        fields, annotations = self._get_api_fields()
        return self.values(*fields, **annotations)

    def to_dataframe(self):
        fields, annotations = self._get_api_fields()
        qs = self.api_values()
        lc_fields = [f.lower() for f in fields]
        return pd.DataFrame.from_records(list(qs), columns=lc_fields, coerce_float=True)

"""Model manager for managing API queries"""
class ApiManager(models.Manager):

    def get_queryset(self):
        return ApiQuerySet(self.model)

    def api_values(self):
        return self.get_queryset().api_values()

    def to_dataframe(self):
        return self.get_queryset().to_dataframe()

class AnimalQuerySet(ApiQuerySet):

    def api_values(self):
        fields, annotations = self._get_api_fields()
        qs = self.values(*fields, **annotations)
        return list(map(self._lower_keys, qs))

class AnimalManager(ApiManager):

    def get_queryset(self):
        return AnimalQuerySet(self.model)