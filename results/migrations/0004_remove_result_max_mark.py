# Generated by Django 4.0 on 2022-01-05 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_alter_result_test_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='max_mark',
        ),
    ]
