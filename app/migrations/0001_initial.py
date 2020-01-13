# Generated by Django 3.0.2 on 2020-01-13 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('code', models.TextField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('code', models.TextField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('nutrition_score', models.IntegerField()),
                ('nutrition_grade', models.CharField(max_length=1)),
                ('energy_100g', models.IntegerField()),
                ('energy_unit', models.TextField()),
                ('carbohydrates_100g', models.FloatField()),
                ('sugars_100g', models.FloatField()),
                ('fat_100g', models.FloatField()),
                ('saturated_fat_100g', models.FloatField()),
                ('salt_100g', models.FloatField()),
                ('sodium_100g', models.FloatField()),
                ('fiber_100g', models.FloatField()),
                ('proteins_100g', models.FloatField()),
                ('thumbnail_url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product')),
            ],
            options={
                'unique_together': {('category', 'product')},
            },
        ),
    ]
