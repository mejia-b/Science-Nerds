# Generated by Django 4.1.4 on 2022-12-26 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_order_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='note',
        ),
    ]