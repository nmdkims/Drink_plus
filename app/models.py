from django.db import models


class Img(models.Model):
    Img = models.FileField(upload_to='uploads/%Y%m%d')
