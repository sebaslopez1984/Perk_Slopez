# Generated by Django 4.0.3 on 2022-03-28 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=100)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idCompany', models.IntegerField(max_length=10)),
                ('company', models.CharField(max_length=100)),
                ('price', models.IntegerField(max_length=10)),
                ('date', models.CharField(max_length=16)),
                ('status_transaction', models.CharField(max_length=12)),
                ('status_approved', models.CharField(max_length=5)),
            ],
        ),
    ]