from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200) 
    description = models.TextField(null=False)
    image = models.ImageField(default='pics/default-post-pic.png',upload_to='pics',null=False)
    mode = models.BooleanField()
