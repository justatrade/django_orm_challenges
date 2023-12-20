# Generated by Django 4.2.3 on 2023-12-09 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=256)),
                ('year_of_production', models.IntegerField()),
                ('ram', models.CharField(max_length=64)),
                ('hdd', models.CharField(max_length=64)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
