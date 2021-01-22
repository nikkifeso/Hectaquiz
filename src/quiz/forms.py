from .models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username',)

class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('email','username')