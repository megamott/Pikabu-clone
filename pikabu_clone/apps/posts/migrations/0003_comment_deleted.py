# Generated by Django 3.2.6 on 2021-09-02 04:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='has this comment been deleted?'),
        ),
    ]
