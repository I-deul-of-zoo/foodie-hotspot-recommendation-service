# Generated by Django 4.2.7 on 2023-12-01 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodiehotspots', '0003_alter_rate_restaurant_alter_rate_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='score',
            new_name='average_score',
        ),
    ]
