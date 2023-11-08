# Generated by Django 4.2.7 on 2023-11-03 22:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sgg', models.CharField(max_length=100, null=True)),
                ('sgg_code', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('start_date', models.CharField(blank=True, max_length=100, null=True)),
                ('business_state', models.CharField(blank=True, max_length=100, null=True)),
                ('closed_date', models.CharField(blank=True, max_length=100, null=True)),
                ('local_area', models.CharField(blank=True, max_length=100, null=True)),
                ('water_facility', models.CharField(blank=True, max_length=100, null=True)),
                ('male_employee_cnt', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.CharField(blank=True, max_length=100, null=True)),
                ('multi_used', models.CharField(blank=True, max_length=100, null=True)),
                ('grade_sep', models.CharField(blank=True, max_length=100, null=True)),
                ('total_area', models.CharField(blank=True, max_length=100, null=True)),
                ('female_employee_cnt', models.CharField(blank=True, max_length=100, null=True)),
                ('buisiness_site', models.CharField(blank=True, max_length=100, null=True)),
                ('sanitarity', models.CharField(blank=True, max_length=100, null=True)),
                ('food_category', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_cnt', models.CharField(blank=True, max_length=100, null=True)),
                ('address_lotno', models.CharField(max_length=200, null=True)),
                ('address_roadnm', models.CharField(max_length=200, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=100, null=True)),
                ('longitude', models.CharField(default=0, max_length=100)),
                ('latitude', models.CharField(default=0, max_length=100)),
                ('name_address', models.CharField(max_length=300, unique=True)),
                ('score', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('content', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodiehotspots.restaurant')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
