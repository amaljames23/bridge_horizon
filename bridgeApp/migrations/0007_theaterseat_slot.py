# Generated by Django 4.1 on 2025-02-04 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bridgeApp', '0006_alter_audience_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='theaterseat',
            name='slot',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bridgeApp.screeningslot'),
        ),
    ]
