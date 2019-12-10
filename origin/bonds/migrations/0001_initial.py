# Generated by Django 2.2.4 on 2019-12-10 10:38

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isin', models.CharField(max_length=250)),
                ('size', models.BigIntegerField()),
                ('currency', djmoney.models.fields.CurrencyField(default='XYZ', max_length=3)),
                ('maturity', models.DateField()),
                ('lei', models.CharField(max_length=250)),
                ('legal_name', models.CharField(max_length=250, null=True)),
            ],
        ),
    ]
