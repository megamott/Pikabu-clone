# Generated by Django 3.2.6 on 2021-09-02 04:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0003_comment_deleted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='text',
        ),
    ]
