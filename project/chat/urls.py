from django.urls import path, re_path
from .views import DialogsView, Users, userprofile, CreateDialogView, MessagesView, createuser, CreateProfile


urlpatterns = [
    path('dialogs/', DialogsView.as_view(), name='dialogs'),
    path('users/', Users.as_view(), name='users'),
    path('dialogs/createuser', userprofile, name='create_user'),
    path('createuserprofile', CreateProfile.as_view(), name='create_profile'),
    re_path(r'^dialogs/create/(?P<user_id>\d+)/$', CreateDialogView.as_view(), name='create_dialog'),
    re_path(r'^dialogs/(?P<chat_id>\d+)/$', MessagesView.as_view(), name='messages'),
]