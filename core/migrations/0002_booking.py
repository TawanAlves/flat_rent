# Generated by Django 4.1.7 on 2024-07-30 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateTimeField(blank=True, null=True)),
                ('checkout', models.DateTimeField(blank=True, null=True)),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='core.flat')),
            ],
        ),
    ]
