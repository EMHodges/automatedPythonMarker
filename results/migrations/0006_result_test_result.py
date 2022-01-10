# Generated by Django 4.0 on 2022-01-05 14:54

from django.db import migrations, models
from results.results_enum import ResultsEnum


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_remove_result_test_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='test_result',
            field=models.CharField(choices=[(ResultsEnum['SUCCESS'], 'SUCCESS'), (ResultsEnum['FAIL'], 'FAIL'), (ResultsEnum['ERROR'], 'ERROR')], default=ResultsEnum['ERROR'], max_length=10),
        ),
    ]
