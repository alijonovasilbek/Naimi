# Generated by Django 5.0.6 on 2024-06-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_category', '0002_alter_maincategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='middlecategory',
            name='middle_image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]