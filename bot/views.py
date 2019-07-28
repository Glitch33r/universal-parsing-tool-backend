import pdb

from main.util import Spider
from .forms import *
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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


def bot_update_view(request, pk: int):
    obj_bot = get_object_or_404(Bot, pk=pk)
    bot = BotFormUpdate(request.POST or None, instance=obj_bot, prefix="bot")

    obj_code = get_object_or_404(Code, bot=obj_bot)
    code = CodeForm(request.POST or None, instance=obj_code, prefix="code")

    if request.method == 'POST':
        if bot.is_valid() and code.is_valid():
            bot.save()
            code.save()
            messages.success(
                request,
                'Bot {} was updated successfully!'.format(bot.cleaned_data['name'])
            )
            return redirect(reverse('bot:bot-list'))

    return render(request, 'bot/bot_update.html', {'bot': bot, 'code': code})


def bot_delete_view(request, obj_id: int):
    obj = get_object_or_404(Bot, pk=obj_id)
    obj.delete()

    return redirect(reverse('bot:bot-list'))


def bot_code_list_view(request):
    object_list = Code.objects.all()
    data = helper_for_pagination(request, Paginator(object_list, 10))

    return render(request, 'code/list/code_list.html', {'object_list': data})


def bot_function_docs(request):
    s = Spider('')
    arr = []
    for func in s.get_all_funcs:
        arr.append(
            {
                'name': func,
                'doc': getattr(Spider, func).__doc__
            }
        )

    return render(request, 'documentation/index.html', {'object_list': arr})


def run_bot(request, pk: int):
    obj = get_object_or_404(Bot, pk=pk)
    code = Code.objects.get(bot=obj)

    existed_log = Log.objects.filter(bot_id=obj.id)
    if existed_log:
        for i in existed_log:
            i.delete()

    s = Spider(url=obj.link, id=pk)
    s._get_tree_from_request()
    try:
        s.parse(code.code)
    except:
        return redirect(reverse('bot:bot-log'))

    Data(bot_id=obj.id, data=s.data_to_json).save()
    Log(bot_id=obj.id, message=f'Bot {obj.name} completed his work', level='S').save()

    return redirect(reverse('bot:bot-log'))


def log_list(request):
    objs_list = Log.objects.all()

    return render(request, 'log/list/log_list.html', {'logs': objs_list})


def bot_data(request):
    obj_list = Data.objects.all()

    return render(request, 'data/list/list.html', {'object_list': obj_list})

