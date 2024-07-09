# Generated by Django 5.0.6 on 2024-07-09 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_customer_code_uztracking_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmenttracking',
            name='flight',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uztracking',
            name='flight',
            field=models.PositiveIntegerField(blank=True, default=11),
            preserve_default=False,
        ),
    ]