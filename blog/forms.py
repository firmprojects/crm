from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'image', 'status', 'body']
        # widgets = {
        #     'warranty_end': DateInput(format='%m-%d-%Y'),
        #     'purchase_date': DateInput(format='%m-%d-%Y'),