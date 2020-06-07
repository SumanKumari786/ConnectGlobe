from django import forms
from django.contrib.auth.models import User
from .models import MyProfile, Post, PostComment, Discussion


class UserUpdate(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = MyProfile
        fields = ['image', 'birth_date', 'phone_number', 'city', 'state', 'bio']


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'slug', 'content', 'file']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here!!!', 'rows':'5', 'cols':'45'}))
    class Meta:
        model = PostComment
        fields = ['comment']


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class':'textarea','placeholder': 'What\'s on your mind ?'})
