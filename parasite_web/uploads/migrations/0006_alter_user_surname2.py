# Generated by Django 4.1 on 2023-03-20 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0005_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='surname2',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
