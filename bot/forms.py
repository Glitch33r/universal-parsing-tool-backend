from django import forms
from .models import *


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['name', 'creator', 'type', 'link']

    def clean_creator(self):
        return self.cleaned_data['creator']

    def clean_name(self):
        data = self.cleaned_data['name']

        if Bot.objects.filter(name=data).exists():
            raise forms.ValidationError('A Bot name already exists. It mast be uniq.')

        return data


class BotFormUpdate(forms.ModelForm):
    disabled_fields = ('name', 'creator',)

    class Meta:
        model = Bot
        fields = ['name', 'creator', 'type', 'link']

    def __init__(self, *args, **kwargs):
        super(BotFormUpdate, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True


class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['title', 'code']
