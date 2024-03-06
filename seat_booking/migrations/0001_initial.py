# Generated by Django 4.2.7 on 2024-03-03 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('passenger', '0001_initial'),
        ('train', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeatBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('is_confirmed', models.BooleanField(default=False)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passenger.passenger')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train.train')),
            ],
        ),
    ]
