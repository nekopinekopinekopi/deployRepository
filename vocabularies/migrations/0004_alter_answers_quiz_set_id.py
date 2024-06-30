# Generated by Django 4.1 on 2024-06-23 07:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vocabularies', '0003_answers_quiz_set_id_answers_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='quiz_set_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
