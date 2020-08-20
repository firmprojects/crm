from django import forms
from .models import Blog
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'image', 'publish', 'body', 'author']
        widgets = {
        #     'warranty_end': DateInput(format='%m-%d-%Y'),
        #     'purchase_date': DateInput(format='%m-%d-%Y'),
            'body': SummernoteWidget(),
         }