from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from .models import Book
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import BookForm


def book_create(request):
    form = BookForm()
    context = {'form': form}
    html_form = render_to_string(
        'dashboard/partial_book_create.html', context, request=request, )

    return JsonResponse({'html_form': html_form})


def book_list(request):
    books = Book.objects.all()

    return render(request, 'dashboard/book_list.html', {'books': books})


def superuser_only(function):

    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner


@method_decorator(superuser_only, name='dispatch')
class Home(TemplateView):
    template_name = 'dashboard/index.html'


class Assets(TemplateView):
    template_name = 'dashboard/assets.html'


class Settings(TemplateView):
    template_name = 'dashboard/settings.html'


def add_to_cart(request, slug):
    product = get_object_or_404(slug=slug)
    cart_item = CartItem.objects.create(product=product)
    cart_qs = Cart.objects.filter(user=request.user, is_ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.products.filter(product__slug=product.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
