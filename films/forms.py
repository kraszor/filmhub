from .models import Comment
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rating']
