# Generated by Django 5.0.4 on 2024-04-29 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_user_created_at_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='picture',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.DeleteModel(
            name='picture',
        ),
    ]
