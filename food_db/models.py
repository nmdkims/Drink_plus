from django.db import models

class FoodModel(models.Model):
    class Meta:
        db_table = "food_db"

    category_name = models.CharField(max_length=256, null=True)
    img = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=True)
    price = models.CharField(max_length=256, null=True)
    score = models.CharField(max_length=256, null=True)