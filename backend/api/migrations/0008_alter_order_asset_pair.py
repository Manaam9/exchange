# Generated by Django 4.1.4 on 2023-01-15 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_order_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='asset_pair',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_pair', to='api.assetpair'),
        ),
    ]