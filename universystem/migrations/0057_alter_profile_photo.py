# Generated by Django 4.0.4 on 2022-06-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0056_article_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='https://pythonplatformkz.s3.us-west-2.amazonaws.com/media/images/profile/pfp.png', null=True, upload_to='images/profile'),
        ),
    ]