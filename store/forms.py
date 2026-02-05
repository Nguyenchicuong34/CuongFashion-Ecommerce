from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'rating', 'comment']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên của bạn'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Viết đánh giá của bạn...'}),
        }