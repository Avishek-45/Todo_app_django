from django.forms import ModelForm
from .models import TODO


class Todoform(ModelForm):
    class Meta:
        model=TODO
        fields=['Title','memo','important']