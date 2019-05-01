from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class AccountConfig(AppConfig):
    name = 'Account'
    verbose_name = _('Пользователи (расш.)')

class GroupConfig(AppConfig):
    name = 'Group'
    verbose_name = _('Отряды')

class OrderConfig(AppConfig):
    name = 'Order'
    verbose_name = _('Данные заявок')
