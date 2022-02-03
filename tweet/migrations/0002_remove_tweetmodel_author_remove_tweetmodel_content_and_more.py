# Generated by Django 4.0.1 on 2022-02-01 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetmodel',
            name='author',
        ),
        migrations.RemoveField(
            model_name='tweetmodel',
            name='content',
        ),
        migrations.RemoveField(
            model_name='tweetmodel',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='tweetmodel',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='img',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='item_tags1',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='item_tags2',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='item_tags3',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='sub_item_tag1',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='sub_item_tag2',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='sub_item_tag3',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='sub_item_tag4',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='sub_item_tag5',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='sub_title',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='title',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
