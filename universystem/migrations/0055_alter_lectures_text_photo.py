# Generated by Django 4.0.4 on 2022-06-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0054_alter_article_options_alter_lectures_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lectures_text',
            name='photo',
            field=models.URLField(),
        ),
    ]
