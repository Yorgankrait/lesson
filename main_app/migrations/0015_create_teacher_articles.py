from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_useridea'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Статья для учителей',
                'verbose_name_plural': 'Статьи для учителей',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='teacherresource',
            name='file',
            field=models.FileField(upload_to='teacher_files/', verbose_name='Файл'),
        ),
        migrations.AddField(
            model_name='teacherresource',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='teacherresource',
            name='file_type',
            field=models.CharField(blank=True, max_length=50, verbose_name='Тип файла'),
        ),
        migrations.AddField(
            model_name='teacherresource',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.AddField(
            model_name='teacherresource',
            name='article',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='main_app.teacherarticle', verbose_name='Статья'),
            preserve_default=False,
        ),
    ] 