# Generated by Django 3.0.8 on 2021-03-05 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0002_auto_20210305_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollcource',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
