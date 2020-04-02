# Generated by Django 3.0.5 on 2020-04-02 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_auto_20200402_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=20, verbose_name='user login name')),
                ('password', models.CharField(max_length=20, verbose_name='user password')),
                ('role', models.CharField(max_length=20, verbose_name='role of user')),
            ],
        ),
    ]
