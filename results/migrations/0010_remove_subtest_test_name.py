# Generated by Django 4.0 on 2022-02-04 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0009_subtest_test_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtest',
            name='test_name',
        ),
    ]