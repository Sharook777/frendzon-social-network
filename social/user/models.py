from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
#from feeds.models import Post

from social.utils import create_shortcode
def upload_imagesTo(instance, filename):
    #user = Shortcode.objects.get(firstname=instance)
    #print("user ",user)
    filename, ext = filename.split(".")
    name = create_shortcode(instance)
    #Shortcode.objects.create(user=instance,shortcode=name)
    #print("user ",user.shortcode)
    #user.shortcode = name
    #print("user ",user.shortcode)
    #print(user.save())
    return "%s/profile picture/%s.%s" %(instance.username, name, ext)

class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=10, primary_key=True,unique=True)
    firstname = models.CharField(max_length=120, null=False, blank=False)
    lastname = models.CharField(max_length=120, null=True, blank=True)
    gender = models.CharField(max_length=10, null=False, blank=False)
    mail_id = models.EmailField(null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=16, null=False, blank=False)
    dob = models.DateField(null=True, blank=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    profile_pic = models.FileField(upload_to=upload_imagesTo, null=True, blank=True)
    auth = models.BooleanField(default=False)
    
    #shortcode = models.CharField(max_length=20, unique=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.firstname
        #return self.user
    
    def get_url_name(self):
        print("Users Model PKuser",self.user.pk)
        return self.pk
        #return reverse("profile", kwargs={"pk":self.slug})
    
    class Meta:
        ordering = ['firstname']
        
'''class Shortcode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    shortcode = models.CharField(max_length=20, unique=True, null=True, blank=True) 
    
    def __str__(self):
        return str(self.shortcode)'''
