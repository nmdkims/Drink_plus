# Generated by Django 4.0.1 on 2022-02-03 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('img', models.CharField(max_length=255)),
                ('sub_title', models.CharField(max_length=30)),
                ('item_tags1', models.CharField(max_length=30)),
                ('item_tags2', models.CharField(max_length=30)),
                ('item_tags3', models.CharField(max_length=30)),
                ('sub_item_tag1', models.CharField(max_length=30)),
                ('sub_item_tag2', models.CharField(max_length=30)),
                ('sub_item_tag3', models.CharField(max_length=30)),
                ('sub_item_tag4', models.CharField(max_length=30)),
                ('sub_item_tag5', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'test',
            },
        ),
    ]