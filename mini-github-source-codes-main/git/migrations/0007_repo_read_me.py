# Generated by Django 4.0 on 2022-03-22 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0006_gituser_has_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='repo',
            name='read_me',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
