# Generated by Django 4.0.2 on 2022-03-26 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_questioncomposite_part_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questioncomposite',
            name='part_name',
        ),
        migrations.AddField(
            model_name='subquestioncomposite',
            name='part_name',
            field=models.TextField(default='l'),
            preserve_default=False,
        ),
    ]
