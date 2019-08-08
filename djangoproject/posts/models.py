from django.db import models
from datetime import datetime

# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(datetime.now, blank=True)
    # class Meta:
    #     verbase_name_plural = 'Posts'