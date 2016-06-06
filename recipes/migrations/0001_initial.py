# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 19:54
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='Nazwa składnika')),
                ('price', models.FloatField(default=0, verbose_name='Cena w PLN za 1kg lub 1l')),
            ],
            options={
                'verbose_name': 'Składnik',
                'verbose_name_plural': 'Składniki',
            },
        ),
        migrations.CreateModel(
            name='IngredientDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0, verbose_name='Ilość składnika (kilogramów lub litrów)')),
                ('amount_name', models.CharField(default='', max_length=200, verbose_name='Nazwa ilosci, np. 1 szklanka, 2 łyżeczki')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient', verbose_name='Składnik')),
            ],
            options={
                'verbose_name': 'Dodatkowe dane składnika',
                'verbose_name_plural': 'Dodatkowe dane składników',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('content', tinymce.models.HTMLField()),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(default='images/BNN.jpg', upload_to='images/')),
                ('ingredients', models.ManyToManyField(through='recipes.IngredientDetails', to='recipes.Ingredient')),
            ],
            options={
                'verbose_name': 'Przepis',
                'verbose_name_plural': 'Przepisy',
            },
        ),
        migrations.AddField(
            model_name='ingredientdetails',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Przepis'),
        ),
    ]
