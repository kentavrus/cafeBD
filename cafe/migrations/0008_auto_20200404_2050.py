# Generated by Django 3.0.5 on 2020-04-04 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0007_auto_20200404_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='barist_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='bill',
            name='card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cafe.Card'),
        ),
        migrations.AlterField(
            model_name='billrows',
            name='price',
            field=models.IntegerField(default=0, verbose_name='price of dish'),
        ),
    ]
