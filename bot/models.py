from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Bot(models.Model):
    BOT_TYPE = (
        ('D', 'DEV'),
        ('P', 'PROD'),
    )
    BOT_STATE = (
        ('W', 'WORKING'),
        ('SP', 'STOPPED'),
        ('SR', 'STARTED'),
        ('F', 'FAILED'),
    )
    name = models.CharField(max_length=128, unique=True)
    type = models.CharField(max_length=1, choices=BOT_TYPE)
    currentState = models.CharField(max_length=2, choices=BOT_STATE, blank=True)
    link = models.URLField(blank=False)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True)

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['name', 'createdAt'])
        ]

    def get_absolute_url(self):
        return reverse('bot:bot-list')


class Code(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modifiedAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class Data(models.Model):
    data = models.TextField(blank=True, null=True)
    bot = models.ForeignKey(
        Bot,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )


class Log(models.Model):
    LOG_LEVELS = (
        ('I', 'INFO'),
        ('W', 'WARNING'),
        ('E', 'ERROR'),
        ('S', 'SUCCESS'),
    )

    level = models.CharField(max_length=1, choices=LOG_LEVELS)
    createdAt = models.DateTimeField(auto_now=True,blank=True)
    message = models.TextField(blank=True, null=True)

    bot = models.ForeignKey(
        Bot,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-createdAt']
