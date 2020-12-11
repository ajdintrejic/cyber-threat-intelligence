# Generated by Django 3.1.4 on 2020-12-07 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cti', '0007_auto_20201205_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server_attack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_name', models.CharField(max_length=32)),
                ('filehash', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Log_line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.CharField(max_length=32, null=True)),
                ('requestMethod', models.CharField(max_length=7, null=True)),
                ('path', models.CharField(max_length=512, null=True)),
                ('httpVersion', models.CharField(max_length=32, null=True)),
                ('response', models.CharField(max_length=32, null=True)),
                ('sizeInBytes', models.CharField(max_length=32, null=True)),
                ('ip_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cti.ip')),
            ],
        ),
    ]