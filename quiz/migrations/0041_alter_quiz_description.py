# Generated by Django 4.2.7 on 2023-12-15 07:46

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0040_alter_quiz_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=tinymce.models.HTMLField(max_length=2000),
        ),
    ]