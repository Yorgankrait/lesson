# Generated by Django 4.2.16 on 2024-10-22 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('presentation', models.FileField(upload_to='lessons/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
