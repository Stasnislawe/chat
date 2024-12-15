from django import forms
from .models import Message, UserProfile


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class ProfileForm(forms.ModelForm):

    def has_changed(self, *args, **kwargs):
        changed_data = super().has_changed()
        if not changed_data:
            return False

        relevant_fields = ['name', 'image']
        for field in relevant_fields:
            if field in changed_data:
                return True

        return False

    class Meta:
        model = UserProfile
        fields = ['name',
                  'image']