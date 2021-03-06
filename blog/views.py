from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, DeleteView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Blog
from django.urls import reverse
from .forms import BlogForm


# class CreateBlogView(LoginRequiredMixin, CreateView):
#     model = Blog
#     template_name = 'blog/add_blog.html'
#     form_class = BlogForm

#     def form_invalid(self, form):
#         form.instance.author = self.request.user
#         return super().form_invalid(form)


def create_blog(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(reverse("blog:blog_view"))
    return render(request, 'blog/add_blog.html', {'form':form})



class UpdateBlogView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    template_name = 'blog/add_blog.html'

    def form_invalid(self, form):
        form.instance.author = self.request.user
        return super().form_invalid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 
 

class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'blog'
    ordering = ['-date']



class BlogDetail(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_view.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(publish=True).order_by('-date')[0:5]
        return context


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 
    

# class Blog(View):
#     def get(self, request):
#         blog = BlogPost.objects.all()
#         form = BlogForm()
#         return render(request, 'blog/blog.html', {'blog':blog, 'form':form})

#     def post(self, request):
#         if request.method == 'POST':
#             form = BlogForm(request.POST)
#             if form.is_valid():
#                 form.save()
#             return HttpResponseRedirect(reverse('blog:blog'))

