from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['title', 'tweet', 'image']  # Include the fields you want to be editable

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tweet': forms.Textarea(attrs={'class': 'form-control'}),
            # Add other widgets as required
        }
