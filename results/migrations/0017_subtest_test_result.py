# Generated by Django 4.0 on 2022-02-17 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0016_remove_subtest_test_result_alter_result_test_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtest',
            name='test_result',
            field=models.CharField(choices=[('SU', 'Success'), ('F', 'Fail'), ('E', 'Error')], default='E', max_length=2),
        ),
    ]