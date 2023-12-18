# Generated by Django 4.2.7 on 2023-11-29 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_question_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.topic'),
        ),
    ]