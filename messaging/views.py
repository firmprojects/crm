from dal import autocomplete

from django.shortcuts import render,reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, TemplateView, FormView
from .forms import MailForm
from .models import MailBody,Mail,Files
from users.models import CustomUser
from django.core.files.storage import default_storage

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

class Inbox(TemplateView):
    template_name='messaging/inbox.html'
    def get(self,request,*args,**kwargs):
        mails = MailBody.objects.filter(to__contains=[request.user.pk])
        print(mails)
        return render(request,self.template_name,{'mails':mails})

class MailView(DetailView):
    template_name='messaging/mail_view.html'
    model = MailBody


class Blog(TemplateView):
    template_name='messaging/blog.html'

class BlogView(TemplateView):
    template_name='messaging/blog_view.html'

class AddBlog(TemplateView):
    template_name='messaging/add_blog.html'

class EditBlog(TemplateView):
    template_name='messaging/edit_blog.html'
