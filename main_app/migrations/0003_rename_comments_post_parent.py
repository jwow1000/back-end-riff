# Generated by Django 5.0.4 on 2024-04-11 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_post_added_alter_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='comments',
            new_name='parent',
        ),
    ]