from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from chat.forms import ProfileForm
from .models import BaseRegisterForm
from chat.models import UserProfile


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = reverse_lazy('login')


class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = ProfileForm
    success_url = reverse_lazy('dialogs')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)