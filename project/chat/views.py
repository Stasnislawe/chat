from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from .forms import MessageForm, ProfileForm
from .models import Chat, UserProfile


# Create your views here.

class Users(TemplateView):
    model = UserProfile
    template_name = 'users.html'

    def get_context_data(self, **kwargs):
        context = super(Users, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class DialogsView(TemplateView):
    model = UserProfile
    profile_form = ProfileForm
    template_name = 'users/dialogs.html'
    success_url = reverse_lazy('dialogs')

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.profile_form
        kwargs['chats'] = Chat.objects.filter(members__in=[self.request.user.id])
        kwargs['user_profile'] = self.request.user
        return super().get_context_data(**kwargs)


def userprofile(request):
    form = ProfileForm(request.POST)
    userprofile = get_object_or_404(UserProfile, user=request.user)

    if form.is_valid():
        form.save(commit=False)
        userprofile.name = form.cleaned_data['name']
        userprofile.image = request.FILES['image']
        userprofile.save()
        return HttpResponseRedirect(reverse_lazy('dialogs'))

    return reverse_lazy('dialogs')


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'users/messages.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if not chats:
            chat = Chat.objects.create()
            chat.members.add(user_id)
            chat.save()
            chat.members.add(request.user)
            chat.save()

        else:
            chat = chats.first()
        return redirect(reverse('messages', kwargs={'chat_id': chat.id}))