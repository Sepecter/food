# Generated by Django 3.1.2 on 2021-03-13 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField(blank=True, max_length=1024, null=True)),
                ('address', models.CharField(choices=[(1, ''), (2, ''), (3, '')], max_length=16)),
                ('likes', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16)),
                ('usertype', models.CharField(choices=[(1, 'student'), (2, 'manager')], max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='img')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.articlepost')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1024)),
                ('created_time', models.TimeField(auto_now=True)),
                ('father_comment', models.CharField(default=0, max_length=16)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.articlepost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.user')),
            ],
        ),
    ]
