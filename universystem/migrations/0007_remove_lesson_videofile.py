# Generated by Django 3.0.8 on 2021-03-09 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0006_lesson_videofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='videofile',
        ),
    ]
