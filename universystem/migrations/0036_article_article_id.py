# Generated by Django 3.0.3 on 2022-04-26 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('universystem', '0035_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='universystem.Lectures'),
        ),
    ]
