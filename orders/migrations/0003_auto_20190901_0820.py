# Generated by Django 2.1.7 on 2019-09-01 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_detail',
            name='size',
            field=models.CharField(choices=[('S', 'Small'), ('L', 'Large')], default='S', max_length=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='prize_large',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Prize for Large'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prize_small',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Prize for Small'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default=None, upload_to='images/', verbose_name='Product Image'),
        ),
    ]
