from django.template import Library
from users.models import CustomUser
from ..models import MailBody
register = Library()

@register.filter(name='get_user')
def get_user(val):
    print(val,CustomUser.objects.values_list('pk'))
    return CustomUser.objects.get(pk=val).username

@register.filter(name='mail_count')
def mail_count(val):
    return len(MailBody.objects.filter(to__contains=[val]))

@register.filter(name='get_reply')
def get_reply(mail_body):
    # print(mail_body)
    return False
    # mail = mail_body.mail
    # print(mail.replies)
    # if mail.replies.__len__() == 0:
    #     return False
    # if mail.replies.__len__() == 1:
    #     return mail_body
    # else:
    #     return MailBody.objects.get(pk=mail.replies[-2])
