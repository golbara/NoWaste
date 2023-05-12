
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='date_of_establishment',
            field=models.DateField(default=datetime.date(2023, 4, 30)),
        ),
    ]
