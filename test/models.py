from django.db import models

class Test(models.Model):
    class Meta:
        db_table = "test"

    test_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    img = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=30)
    item_tags1 = models.CharField(max_length=30)
    item_tags2 = models.CharField(max_length=30)
    item_tags3 = models.CharField(max_length=30)
    sub_item_tag1 = models.CharField(max_length=30)
    sub_item_tag2 = models.CharField(max_length=30)
    sub_item_tag3 = models.CharField(max_length=30)
    sub_item_tag4 = models.CharField(max_length=30)
    sub_item_tag5 = models.CharField(max_length=30)
