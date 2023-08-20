# Generated by Django 4.2.3 on 2023-08-11 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='replies',
        ),
        migrations.AlterField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog'),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('reply', models.TextField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment')),
            ],
        ),
    ]
