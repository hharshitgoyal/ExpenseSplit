# Generated by Django 5.0.2 on 2024-02-10 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExpensesSplitApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
