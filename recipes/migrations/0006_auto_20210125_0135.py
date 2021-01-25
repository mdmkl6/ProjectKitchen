# Generated by Django 3.1.3 on 2021-01-25 00:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_remove_recipe_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='rated_by',
            field=models.ManyToManyField(blank=True, related_name='rated_recipes', through='recipes.UserRating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userrating',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userrating',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recipes.recipe'),
        ),
    ]
