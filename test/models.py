# tweet/models.py
from django.db import models


# Create your models here.
class TestModel(models.Model):
    class Meta:
        db_table = "test"

    category_name = models.CharField(max_length=256, null=True)
    img = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=True)
    price = models.CharField(max_length=256, null=True)
    description = models.CharField(max_length=256, null=True)


