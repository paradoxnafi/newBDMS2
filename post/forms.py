from django.forms import ModelForm
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'address', 'blood_group', 'required_bags', 'deadlineDate', 'deadlineTime', 'contact_number']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
        self.fields['deadlineDate'].widget.input_type = 'date'
        self.fields['deadlineTime'].widget.input_type = 'time'
        self.fields['description'].widget.attrs.update({'rows' : '4'})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'rows': '2'})