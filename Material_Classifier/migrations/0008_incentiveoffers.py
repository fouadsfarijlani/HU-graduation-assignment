# Generated by Django 3.2.3 on 2021-05-31 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Material_Classifier', '0007_auto_20210531_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncentiveOffers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_title', models.CharField(max_length=150)),
                ('offer_type', models.CharField(max_length=150)),
                ('offer_content', models.TextField()),
                ('offer_date_start', models.DateField()),
                ('offer_date_end', models.DateField()),
                ('offer_is_active', models.BooleanField()),
                ('offer_users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
