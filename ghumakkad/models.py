from django.db import models
# Create your models here.
class District(models.Model):
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    lat = models.DecimalField(max_digits=20,decimal_places=8)
    longi = models.DecimalField(max_digits=20,decimal_places=8)
    image_source = models.TextField()
class Place(models.Model):
    state=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    description=models.TextField()
    photo=models.TextField()
class Comments(models.Model):
    state=models.CharField(max_length=50)
    name_district =models.CharField(max_length=50)
    by= models.CharField(max_length=60)
    content= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        ordering=['-created_at']
class Blog(models.Model):
    state=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    by=models.CharField(max_length=50)
    file=models.FileField(upload_to='blog')
    created_at= models.DateTimeField(auto_now_add=True,null=True)
    photo=models.ImageField(upload_to='blog')
    description=models.TextField()
    published=models.CharField(max_length=10)
    class Meta:
        ordering=['-created_at']
class Contact(models.Model):
    by=models.CharField(max_length=50)
    message=models.TextField()
class Sd(models.Model):
    state=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
