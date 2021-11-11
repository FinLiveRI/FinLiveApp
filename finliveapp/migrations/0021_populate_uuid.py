import uuid

from django.db import migrations, models


def populate_uuid(apps, schema_editor):
    _model = apps.get_model('finliveapp', 'Equipment')
    for obj in _model.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('finliveapp', '0020_auto_20211110_1019'),
    ]

    operations = [
        migrations.RunPython(populate_uuid),
    ]
