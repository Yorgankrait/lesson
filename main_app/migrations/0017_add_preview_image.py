from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_update_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherarticle',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='article_previews/', verbose_name='Превью изображение'),
        ),
    ] 