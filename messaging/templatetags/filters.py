from django.template import Library
from users.models import CustomUser
from ..models import MailBody
register = Library()

@register.filter(name='get_user')
def get_user(val):
    print(val,CustomUser.objects.values_list('pk'))
    return CustomUser.objects.get(pk=val).username

@register.filter(name='mail_count')
def mail_count(val,sent=False):
    if sent:
        return len(MailBody.objects.filter(from_email=val,draft = False,trash=False))
    return len(MailBody.objects.filter(to__contains=[val],draft = False,trash=False))

@register.filter(name='read')
def read(mail_body,user):
    return mail_body.open_ed[str(user)]
