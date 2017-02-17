from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from user.models import Users

class PostManager(models.Manager):
    def count_likes(self, instance, count):
        #print("working")
        if isinstance(instance, Post):
            #obj = self.objects.get()
            instance.likes += count
            #print(instance.likes)
            instance.save()
            return instance.likes
        return None
            
    '''def count_dislikes(self, instance):
        if isinstance(User, instance):
            #obj = self.objects.get()
            instance.comments += 1
            instance.save()
        '''
        
from social.utils import create_shortcode     
def upload_imagesTo(instance, filename):
    #print(instance.__class__)
    #print(instance.user)
    
    user=User.objects.get(username=instance.user)
    filename, extension = filename.split(".")
    name = create_shortcode(instance)
    
    #print(instance)
    #print(filename, extension, name)
    #instance.shortcode = name
    #print(instance.shortcode.save())
    #instance.save()
    #print(user, user.username)
    return "%s/post/%s.%s" %(user.username, name, extension)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=10, primary_key=True,unique=True)
    content = models.TextField()
    #image = models.FileField(upload_to=upload_images_to, null=True, blank=True)
    image = models.FileField(upload_to=upload_imagesTo, null=True, blank=True)
    #image = models.ImageField(null=True, blank=True)
    # install pillow for ImageField to work
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    #favourite = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    
    #shortcode = models.CharField(max_length=20, default=None, unique=True, null=True, blank=True)
    #user_like = models.ManyToManyField(Post_like, related_name="like", null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
   
    
   
    def __str__(self):
        return str(self.slug )
    
    def get_absolute_url(self):
        #print("self",self.user)
        #url = Users.get_url_name(self)
        url = Users.objects.get(user=self.user)
        #return "/%s/profile/"%(url.pk)
        return reverse("profile", kwargs={ "member":url.pk })
    
    
    '''def get_likes(self):
        print(Post_like.like)
        if self.like == "L":
            return True
        else:
            return False'''
 
  
    class Meta:
        ordering = ["-timestamp"]

class Post_like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    #post = models.OneToOneField(Post, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.CharField(max_length=10, default=None, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    objects = PostManager()
    
    def __str__(self):
        return str(self.post)
    
    '''def get_likes(self):
        print(self.like)
        if self.like == "L":
            return True
        else:
            return False'''
        
        
    class Meta:
        ordering = ["post", "-updated",]        
