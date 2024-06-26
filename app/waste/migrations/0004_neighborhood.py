# Generated by Django 5.0.1 on 2024-05-10 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0003_alter_wastetransfertosts_volume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=20)),
                ('longitude', models.CharField(max_length=20)),
                ('sts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.sts')),
            ],
        ),
    ]
