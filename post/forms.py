from django.forms import ModelForm
from .models import Post, Comment

from django import forms
#from django.db import models

class PostForm(ModelForm):
#    is_resolved = models.BooleanField(default=False)
    class Meta:
        model = Post
        fields = ['description', 'address', 'blood_group', 'required_bags', 'deadlineDate', 'deadlineTime', 'contact_number', 'is_resolved']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
        self.fields['deadlineDate'].widget.input_type = 'date'
        self.fields['deadlineTime'].widget.input_type = 'time'
        self.fields['contact_number'].widget.input_type = 'number'
        self.fields['description'].widget.attrs.update({'rows' : '4'})
        self.fields['is_resolved'].widget.attrs.update({'class' : 'form-check-input'})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'rows': '2'})


# Post edit from



# class AccountUpdateForm(forms.ModelForm):

#     class Meta:
#         model = RegisterUser
#         fields = {'email', 'username', 'name', 'contact_number', 'address', 'date_of_birth', 'nid', 'blood_group'}

#     def clean_email(self):
#         if self.is_valid():
#             email = self.cleaned_data['email']
#             try:
#                 registeruser = RegisterUser.objects.exclude(pk=self.instance.pk).get(email=email)
#             except RegisterUser.DoesNotExist:
#                 return email
#             raise forms.ValidationError('Email "%s" is already in use' % registeruser.email)