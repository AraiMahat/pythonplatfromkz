# Generated by Django 3.0.8 on 2021-03-21 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0010_profile_adress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollcource',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='enrollcource',
            name='student',
        ),
        migrations.RemoveField(
            model_name='message',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='course',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='image',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='price',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='adress',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='information',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='EnrollCource',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
