# Generated by Django 4.0 on 2022-01-05 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_remove_result_max_mark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='test_result',
        ),
    ]
