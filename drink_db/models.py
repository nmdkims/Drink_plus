# tweet/models.py
from django.db import models


# Create your models here.
class DrinkModel(models.Model):
    class Meta:
        db_table = "drink_db"

    category_name = models.CharField(max_length=256, null=True)
    img = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=True)
    price = models.CharField(max_length=256, null=True)
    description = models.CharField(max_length=256, null=True)
    score = models.CharField(max_length=256, null=True)
    alcohol = models.CharField(max_length=256, null=True)

    style_info = models.CharField(max_length=256, null=True)
    aroma_info = models.CharField(max_length=256, null=True)
    flavor_info = models.CharField(max_length=256, null=True)
    finish_info = models.CharField(max_length=256, null=True)
    smoothness_info = models.CharField(max_length=256, null=True)
    enjoy_info = models.CharField(max_length=256, null=True)
    pairing_info = models.CharField(max_length=256, null=True)

    page = models.CharField(max_length=256, null=True)
