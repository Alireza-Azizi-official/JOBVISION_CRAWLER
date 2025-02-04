from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length = 255)
    company_name = models.CharField(max_length = 255)
    link = models.URLField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'{self.title} at {self.company_name}'
    