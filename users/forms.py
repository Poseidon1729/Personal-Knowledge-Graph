from django.forms import Authen
from .models import Users

class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'bio']