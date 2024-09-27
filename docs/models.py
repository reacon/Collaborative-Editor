from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Documents(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_documents')
    users = models.ManyToManyField(User,related_name='documents')
    user_permissions = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Documents, self).save(*args, **kwargs)
