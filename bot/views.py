from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView, DetailView)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import *
from django.contrib import messages
import pdb
from django.http import JsonResponse


def bot_list_view(request):
    object_list = Bot.objects.all()
    data = helper_for_pagination(request, Paginator(object_list, 10))

    if request.is_ajax():
        if request.GET.get('search'):
            text_to_search = request.GET.get('search')
            return JsonResponse(
                {
                    'type': 'search',
                    'response': render_to_string('bot/list/bot_element.html', {'object_list': Bot.objects.filter(
                        name__contains=text_to_search)})
                }
            )
        elif not request.GET.get('search'):
            data = helper_for_pagination(request, Paginator(object_list, 10))
            return JsonResponse(
                {
                    'type': 'default',
                    'response': render_to_string('bot/list/bot_element.html', {'object_list': data})
                }
            )

    return render(request, 'bot/list/bot_list.html', {'object_list': data})


def helper_for_pagination(request, p: Paginator):
    page = request.GET.get('page')

    try:
        data = p.page(page)
    except PageNotAnInteger:
        data = p.page(1)
    except EmptyPage:
        data = p.page(p.num_pages)

    return data


def bot_create_view(request):
    if request.method == 'POST':
        bot = BotForm(request.POST, prefix="bot")
        code = CodeForm(request.POST, prefix="code")
        if bot.is_valid() and code.is_valid():
            bot_obj = bot.save()
            messages.success(
                request,
                'Bot {} was created successfully!'.format(bot.cleaned_data['name'])
            )
            action = code.save(commit=False)
            action.bot = bot_obj
            action.save()

            messages.success(
                request,
                'Code for bot {} was created successfully!'.format(bot.cleaned_data['name'])
            )

            return redirect(reverse('bot:bot-list'))
    else:
        bot = BotForm(prefix="bot", initial={'creator': request.user, 'type': 'D'})
        code = CodeForm(prefix="code", initial={'code': 'Your code here :)'})

    return render(request, 'bot/bot_create.html', {'bot': bot, 'code': code})


def bot_update(request, pk):
    obj_bot = get_object_or_404(Bot, pk=pk)
    bot = BotForm(request.POST or None, instance=obj_bot)
    obj_code = get_object_or_404(Code, bot=obj_bot)
    code = CodeForm(request.POST or None, instance=obj_code)
    if bot.is_valid() and code.is_valid():
        bot.save()
        code.save()
        messages.success(
            request,
            'Bot {} was updated successfully!'.format(bot.cleaned_data['name'])
        )
        return redirect(reverse('bot:bot-list'))

    return render(request, 'bot/bot_update.html', {'bot': bot, 'code': code})


def bot_delete(request, obj_id: int):
    obj = get_object_or_404(Bot, pk=obj_id)
    obj.delete()
    return redirect(reverse('bot:bot-list'))


# class BotDeleteView(DeleteView):
#     model = Bot
#     # pdb.set_trace()
#
#     def get_success_url(self):
#         return reverse('bot:bot-list')


class BotUpdateView(SuccessMessageMixin, UpdateView):
    model = Bot
    fields = ['creator', 'type', 'link']
    template_name = 'bot/bot_update.html'
    success_message = 'Bot was updated successfully'

    def get_success_url(self):
        return reverse('bot:bot-list')
