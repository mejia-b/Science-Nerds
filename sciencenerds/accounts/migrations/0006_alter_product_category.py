# Generated by Django 4.1.4 on 2022-12-22 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_order_tags_product_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Clothing and Accessories', 'Clothing and Accessories'), ('Drinkware', 'Drinkware')], max_length=200, null=True),
        ),
    ]