from django.forms import ModelForm
from .models import News

class TodoForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'info', 'image', 'url']