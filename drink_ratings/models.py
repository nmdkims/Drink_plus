from django.db import models

class Drink_Rating_Model(models.Model):
    class Meta:
        db_table = "drink_ratings"

    drinkid = models.CharField(max_length=256, null=True)
    score = models.CharField(max_length=256, null=True)
    timestamp = models.CharField(max_length=256, null=True)
