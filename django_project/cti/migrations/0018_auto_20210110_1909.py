# Generated by Django 2.2.5 on 2021-01-10 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cti', '0017_auto_20210110_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='security',
            field=models.CharField(choices=[('CF', 'Confidental'), ('S', 'Secret'), ('Top Secret', 'Top Secret')], max_length=2),
        ),
    ]