from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control border-0',
            'placeholder': 'আপনার মনে কী আসছে?',
            'rows': 3,
        }),
        required=False
    )

    class Meta:
        model = Post
        fields = ('content', 'image', 'privacy')
        widgets = {
            'privacy': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'মন্তব্য করুন...',
            })
        }
