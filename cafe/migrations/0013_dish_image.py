# Generated by Django 3.0.5 on 2020-04-21 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0012_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='image',
            field=models.TextField(default=''),
        ),
    ]
