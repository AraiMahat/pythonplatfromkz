# Generated by Django 3.0.8 on 2021-03-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0012_auto_20210321_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('information', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('youtube', models.CharField(max_length=200)),
                ('image', models.ImageField(null=True, upload_to='images/lesson')),
                ('document', models.FileField(null=True, upload_to='pdf/document')),
            ],
        ),
    ]
