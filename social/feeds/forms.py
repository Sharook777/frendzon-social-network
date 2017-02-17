from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]
        
        '''def save(self):
            super(PostForm, self).save()
            user = request.user'''