
# Create your models here.

from django.db import models

class User(models.Model):
    USER_TYPE_CHOICES = (
        (1,'student'),
        (2,'manager'),
    )
    username = models.CharField(max_length=16)
    usertype = models.CharField(choices=USER_TYPE_CHOICES,max_length=16)
    #password = models.CharField(max_length=16)
    #token = models.CharField(max_length=64)

class ArticlePost(models.Model):
    ADDRESS_TYPE_CHOICES = (
        (1, ''),
        (2, ''),
        (3, ''),
    )
    poster = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=1024,null=True,blank=True)
    address = models.CharField(choices=ADDRESS_TYPE_CHOICES,max_length=16)
    comments = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    article = models.ForeignKey("ArticlePost",on_delete=models.CASCADE)
    #user = models.ForeignKey('User',on_delete=models.CASCADE)
    poster = models.CharField(max_length=32,default=0)
    comment = models.TextField(max_length=1024)
    created_time = models.TimeField(auto_now=True)
    father = models.CharField(max_length=16,default=0)
    likes = models.IntegerField(default=0)

class Like(models.Model):
    comment = models.ForeignKey("Comment",on_delete=models.CASCADE)
    user = models.CharField(max_length=16)

class ImgToArticle(models.Model):
    article = models.ForeignKey('ArticlePost',on_delete=models.CASCADE)
    img = models.ImageField(upload_to="img")

class ImgToComment(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    img = models.ImageField(upload_to="img")

