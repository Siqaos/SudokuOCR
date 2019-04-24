from django.db import models

# Create your models here.
class Post(models.Model):
    cover = models.ImageField(upload_to='images/')
