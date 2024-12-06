from django import forms
from .models import Message, UserProfile


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name',
                  'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
