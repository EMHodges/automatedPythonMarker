# Generated by Django 4.0.2 on 2022-03-17 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_alter_subquestioncomposite_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subquestioncomposite',
            name='answer',
        ),
    ]
