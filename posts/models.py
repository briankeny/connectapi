from django.db import models
from django.utils import timezone
from  authentication.models import User
from django.contrib.postgres.fields import ArrayField

class Post(models.Model):
    category_choices = (
        ('news', 'News'),
        ('post', 'Post'),
        ('education', 'Education'),
        ('announcement', 'Announcement')
    )
    post_id=models.AutoField(primary_key=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=False,default=None)
    category = models.CharField(max_length=100,choices=category_choices,default='post')
    title = models.CharField(max_length=100,default=None,null=True,blank=True)
    content = models.TextField(null=False ,default="",max_length=500)
    images = ArrayField(models.CharField( max_length=300, default=None,null=True, blank=True),null=True,blank=True,default=None)
    document  = models.FileField(upload_to='post_documents', null=True, blank=True)
    video = models.FileField(upload_to='post_videos', null=True, blank=True)
    timestamp =  models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.post_id} -{self.owner.first_name}'


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(null=False, default="", max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'{self.owner.first_name}'

 
class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False, default="", max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.first_name}'

