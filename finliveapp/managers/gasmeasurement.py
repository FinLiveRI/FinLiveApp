#from finliveapp.models import GasMeasurement, Animal, Equipment, Organization, Barn
import json

import pandas as pd
from finliveapp import models
import django.db
import json
import datetime

def _total_seconds(t):
    return int(datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds())

class GasMeasurementManager(django.db.models.Manager):

    def create_measurements(self, data, organizationid, farmid):
        fields = ('organization', 'barn', 'equipment', 'rfid', 'start_time', 'end_time',
                  'measurement_duration', 'co2', 'ch4', 'o2', 'h2', 'airflow', 'airflow_cf', 'wind_speed',
                  'wind_direction', 'wind_cf')
        # animals = Animal.objects.filter(barn__farmid=farmid).all()
        equipment = models.Equipment.objects.filter(barn__farmid=farmid).all()
        barn = models.Barn.objects.get(farmid=farmid)
        org = models.Organization.objects.get(id=organizationid)
        events = []
        for visit in data:
            # visit["animal"] = animals.get(euid=visit["euid"])
            visit["equipment"] = equipment.get(equipmentid=visit["equipmentid"])
            visit["barn"] = barn
            visit["organization"] = org
            events.append(models.GasMeasurement(**{f: visit[f] for f in fields}))
        return events

    """Read greenfeed visit data from Excel"""
    def read_greenfeed(self, file):
        df = pd.read_excel(file, sheet_name="Visit_Data", skiprows=1)
        df = df.rename(mapper=lambda x: x.lower().replace(" ", "_").replace("_(g/d)", "").replace("_(l/s)", ""), axis=1)
        df["measurement_duration"] = [_total_seconds(gd) for gd in df.total_time_with_good_data]
        df = df.rename({'unit_id': 'equipmentid', 'rfid_number': 'rfid',
                        'wind_sp': 'wind_speed', 'wind_dir': 'wind_direction'},
                       axis=1)
        #TODO investigate if to_dict is faster
        return json.loads(df[['rfid', 'equipmentid', 'start_time', 'end_time',
                   'measurement_duration', 'co2', 'ch4', 'o2', 'h2', 'airflow', 'airflow_cf', 'wind_speed',
                   'wind_direction', 'wind_cf']].to_json(orient="records", date_format="iso"))
