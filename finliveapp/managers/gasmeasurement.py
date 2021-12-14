#from finliveapp.models import GasMeasurement, Animal, Equipment, Organization, Barn
from finliveapp import models
import django.db

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
