# tweet/models.py
from django.db import models
from user.models import UserModel


# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    title = models.CharField(max_length=256, null=True)
    img = models.CharField(max_length=256, null=True)
    sub_title = models.CharField(max_length=256, null=True)
    item_tags1 = models.CharField(max_length=256, null=True)
    item_tags2 = models.CharField(max_length=256, null=True)
    item_tags3 = models.CharField(max_length=256, null=True)
    sub_item_tag1 = models.CharField(max_length=256, null=True)
    sub_item_tag2 = models.CharField(max_length=256, null=True)
    sub_item_tag3 = models.CharField(max_length=256, null=True)
    sub_item_tag4 = models.CharField(max_length=256, null=True)
    sub_item_tag5 = models.CharField(max_length=256, null=True)
