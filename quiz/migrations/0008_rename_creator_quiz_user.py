# Generated by Django 4.2.7 on 2023-11-29 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_rename_user_quiz_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='creator',
            new_name='user',
        ),
    ]
