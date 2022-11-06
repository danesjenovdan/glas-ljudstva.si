# Generated by Django 4.1.2 on 2022-10-21 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zahteve', '0023_alter_demand_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='demand',
            name='municipality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='zahteve.municipality'),
        ),
        migrations.AddField(
            model_name='party',
            name='municipality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='zahteve.municipality'),
        ),
    ]