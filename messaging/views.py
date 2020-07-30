from dal import autocomplete
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render,reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, TemplateView, FormView
from .forms import MailForm,ReplyForm
from .models import MailBody,Mail,Files,Trash
from users.models import CustomUser
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
import json

class EmailAutocompletesView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = CustomUser.objects.all().order_by('-id')
        if self.q:
            qs = qs.filter(email__istartswith=self.q)
        return qs


class Compose(FormView):
    template_name='messaging/compose.html'
    form_class = MailForm
    success_url = reverse_lazy('messaging:compose')
    def form_valid(self, form):
        data = form.cleaned_data
        mail_b = MailBody(to=data['to'],cc=data['cc'],subject=data['subject'],body=data['body'],from_email=self.request.user.pk)
        mail_b.save()
        for file in self.request.FILES.getlist('attachments'):
            file_name = default_storage.save(file.name, file)
            Files.objects.create(file=file_name,mail=mail_b)

        if self.request.POST.get('draft') == 'on':
            mail_b.draft = True
            mail_b.save()
        else:
            mail = Mail.objects.create(body=mail_b,)
        return super(Compose, self).form_valid(form)

class ReplyView(FormView):
    template_name='messaging/reply.html'
    form_class = ReplyForm
    success_url = reverse_lazy('messaging:compose')
    def get(self,request,**kwargs):
        super().get(request,**kwargs)
        mail = MailBody.objects.get(pk=int(self.kwargs['pk']))
        cont = self.get_context_data()
        cont['mail'] = mail
        return render(request,self.template_name,cont)

    def form_valid(self, form):
        data = form.cleaned_data
        mail_body = MailBody.objects.get(pk=int(self.kwargs['pk']))

        mail = mail_body.mail
        mail_b = MailBody(to=[mail_body.from_email],cc=data['cc'],subject=data['subject'],body=data['body'],from_email=self.request.user.pk)
        mail_b.save()
        for file in self.request.FILES.getlist('attachments'):
            file_name = default_storage.save(file.name, file)
            Files.objects.create(file=file_name,mail=mail_b)

        arr = mail.replies
        arr.append(mail_b.pk)
        mail.replies = arr
        mail.save()
        mail = Mail.objects.create(body=mail_b,)
        return super(ReplyView, self).form_valid(form)

class Inbox(TemplateView):
    template_name='messaging/inbox.html'
    def get(self,request,*args,**kwargs):
        mails = MailBody.objects.filter(to__contains=[request.user.pk],draft = False,trash=False).order_by('-date')
        return render(request,self.template_name,{'mails':mails})

class Sent_mail(TemplateView):
    template_name='messaging/sent.html'
    def get(self,request,*args,**kwargs):
        mails = MailBody.objects.filter(from_email=request.user.pk,draft = False,trash=False).order_by('-date')
        return render(request,self.template_name,{'mails':mails})

class Draft(TemplateView):
    template_name='messaging/draft.html'
    def get(self,request,*args,**kwargs):
        mails = MailBody.objects.filter(from_email=request.user.pk,draft = True,trash=False).order_by('-date')
        return render(request,self.template_name,{'mails':mails})
class Trash_(TemplateView):
    template_name='messaging/trash.html'
    def get(self,request,*args,**kwargs):
        # mails = MailBody.objects.filter(from_email=request.user.pk,trash=True).order_by('-date')
        mails = Trash.objects.get(user=request.user).body.order_by('-date')

        return render(request,self.template_name,{'mails':mails})


class MailView(DetailView):
    template_name='messaging/mail_view.html'
    model = MailBody
    def get(self,request,**kwargs):
        super().get(request,**kwargs)
        self.object = self.get_object()
        cont = self.get_context_data()
        cont['reply_form'] = ReplyForm
        return render(request,self.template_name,cont)

class MailViewSent(DetailView):
    template_name='messaging/mail_view_sent.html'
    model = MailBody
    def get(self,request,**kwargs):
        super().get(request,**kwargs)
        self.object = self.get_object()
        cont = self.get_context_data()
        cont['reply_form'] = ReplyForm
        return render(request,self.template_name,cont)

class Blog(TemplateView):
    template_name='messaging/blog.html'

class BlogView(TemplateView):
    template_name='messaging/blog_view.html'

class AddBlog(TemplateView):
    template_name='messaging/add_blog.html'

class EditBlog(TemplateView):
    template_name='messaging/edit_blog.html'


@login_required
def forward_view(request,pk):
    if request.method == 'POST':
        mail_b = MailBody.objects.get(pk=pk)
        mail__ = MailBody.objects.create(to=request.POST.getlist('to'),subject=mail_b.subject,body=mail_b.body,from_email=request.user.pk)

        for i in mail_b.files_set.all():
            Files.objects.create(file=i.file,mail=mail__)
        mail = Mail.objects.create(body=mail__,)
        return HttpResponseRedirect(reverse('messaging:mail_view',args=(pk,)))

@login_required
def mark_as_read(request,pk):
    mail_b = MailBody.objects.get(pk=pk)
    mail_b.open_ed[str(request.user.pk)] = True
    mail_b.save()
    return JsonResponse({})

@login_required
def move_to_trash(request,pk):
    mail_b = MailBody.objects.get(pk=pk)
    mail_b.trash = True
    mail_b.save()
    try:
        trash = Trash.objects.get(user=request.user)
        trash.body.add(mail_b)

    except Trash.DoesNotExist:
        trash = Trash.objects.create(user=request.user)
        trash.body.add(mail_b)
    return HttpResponseRedirect(reverse('messaging:inbox'))

@login_required
def move_to_trash_multiple(request):
    if request.method == 'POST':
        for pk in json.loads(request.POST['data'])['data']:
            mail_b = MailBody.objects.get(pk=int(pk))
            mail_b.trash = True
            mail_b.save()
            try:
                trash = Trash.objects.get(user=request.user)
                trash.body.add(mail_b)

            except Trash.DoesNotExist:
                trash = Trash.objects.create(user=request.user)
                trash.body.add(mail_b)
    return JsonResponse({})

@login_required
def empty_trash(request):
    try:
        trash = Trash.objects.get(user=request.user)
        # for i in trash.body.all(): i.delete()
        trash.body.clear()

    except Trash.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('messaging:trash_mail'))
