# Generated by Django 4.0.4 on 2022-04-29 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0044_alter_article_body1_alter_article_body2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='topic1',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='topic2',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='topic3',
            field=models.TextField(blank=True),
        ),
    ]
