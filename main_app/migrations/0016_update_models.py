from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_create_teacher_articles'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacherresource',
            options={'ordering': ['order', 'created_at'], 'verbose_name': 'Файл для учителей', 'verbose_name_plural': 'Файлы для учителей'},
        ),
        migrations.AlterField(
            model_name='teacherarticle',
            name='content',
            field=models.TextField(blank=True, verbose_name='Содержание'),
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='article_images/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main_app.teacherarticle')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ] 