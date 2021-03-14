from django.db import models

# Create your models here.
class User(models.Model):
    ID=models.IntegerField(auto_created=True,primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=254)
    password=models.CharField(max_length=128)
    bio =models.TextField(blank=True, default='')
    image =models.ImageField(upload_to="images",default='images/profile.png')
    
class Movie(models.Model):
    ID=models.IntegerField(auto_created=True,primary_key=True)
    name=models.CharField(max_length=50)
    releasedDate=models.DateField()
    production=models.CharField(max_length=50)
    duration=models.TimeField()
    plot=models.TextField()
    image=models.ImageField(upload_to="images")
    rating=models.FloatField(default=0.0)

class Review(models.Model):
    ID=models.IntegerField(auto_created=True,primary_key=True)
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    mid=models.ForeignKey(Movie,on_delete=models.CASCADE)
    reviewText=models.TextField()
    rating=models.FloatField()
    dateTime=models.DateTimeField()