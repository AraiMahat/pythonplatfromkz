# Generated by Django 3.0.8 on 2021-03-05 06:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollcource',
            name='course',
        ),
        migrations.AddField(
            model_name='enrollcource',
            name='lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='universystem.Lesson'),
            preserve_default=False,
        ),
    ]
