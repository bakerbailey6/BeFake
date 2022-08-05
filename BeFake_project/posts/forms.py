from django import forms
from django.db.migrations.state import get_related_models_tuples
from .models import Comments, Post
from django.utils.translation import gettext_lazy as _
from django.db import models

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        

        fields = ['content','parent']
        
        labels = {
            'content': _(''),
        }
        
        widgets = {
            'content' : forms.TextInput(),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['title', 'image']


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)      