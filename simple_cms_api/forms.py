from django.contrib.auth.forms import UserCreationForm as UCrF
from django.contrib.auth.forms import UserChangeForm as UChF

from .models import User


class UserCreationForm(UCrF):

    class Meta(UCrF):
        model = User
        fields = ('email',)


class UserChangeForm(UChF):

    class Meta:
        model = User
        fields = ('email',)
