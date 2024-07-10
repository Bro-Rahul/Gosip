# Generated by Django 5.0.6 on 2024-07-02 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('body', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/images')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('like', models.PositiveIntegerField(blank=True, null=True)),
                ('ok', models.PositiveIntegerField(blank=True, null=True)),
                ('loved', models.PositiveIntegerField(blank=True, null=True)),
                ('dislike', models.PositiveIntegerField(blank=True, null=True)),
                ('angry', models.PositiveIntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='users.publisher')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('body', models.TextField()),
                ('like', models.PositiveIntegerField(blank=True, null=True)),
                ('dislike', models.PositiveIntegerField(blank=True, null=True)),
                ('upvote', models.PositiveIntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.commenter')),
                ('sub_comments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_comment', to='posts.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.CharField(max_length=200)),
                ('user_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread', to='posts.post')),
            ],
            options={
                'unique_together': {('user_post', 'identity')},
            },
        ),
    ]
