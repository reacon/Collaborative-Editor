from django.db import models
from django.utils.text import slugify

# Create your models here.
from django.contrib.auth.models import User

class Documents(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_documents')
    users = models.ManyToManyField(User,through='DocumentsPermissions',related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class DocumentsPermissions(models.Model):
    document = models.ForeignKey('Documents' ,on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)


    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Documents, self).save(*args, **kwargs)

    
# from django.db import models
# from django.utils.text import slugify
# from django.contrib.auth.models import User

# class Documents(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     content = models.TextField(blank=True)
#     creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_documents')
#     users = models.ManyToManyField(User,related_name='documents')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.name
    
#     def save(self,*args,**kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super(Documents, self).save(*args, **kwargs)
