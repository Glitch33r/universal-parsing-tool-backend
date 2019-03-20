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


class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['title', 'code']

    def clean_title(self):
        title = self.cleaned_data['title']
        # bot = self.cleaned_data['bot']

        if Code.objects.filter(title=title).exists():
            raise forms.ValidationError(
                'This title already exists. Please, fix and try again.'
            )

        return title
