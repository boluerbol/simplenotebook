# Generated by Django 5.1.4 on 2024-12-11 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_note_user_alter_note_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='note_images/'),
        ),
    ]
