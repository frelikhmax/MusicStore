from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from app.forms import LoginForm, RegisterForm, SettingsForm
from app.models import MusicProduct, StoreItem, OrderItem, Order

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator


def paginate(objects, request, per_page=5):
    paginator = Paginator(objects, per_page)

    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
        elif page > paginator.num_pages:
            page = paginator.num_pages
    except ValueError:
        page = 1

    return paginator.page(page), page, paginator.num_pages


# Create your views here.

@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def index(request):
    items, page, pages_number = paginate(StoreItem.objects.new(), request, 4)

    return render(request, 'index.html',
                  {'store_items': items, 'page': page, 'prev': page - 1, 'fol': page + 1})


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def add_to_cart_index(request, store_item_id):
    store_item = get_object_or_404(StoreItem, pk=store_item_id)

    if store_item.quantity <= 0:
        return redirect('index')

    order, created_order = Order.objects.get_or_create(user=request.user, is_completed=False)

    order_item, created = OrderItem.objects.get_or_create(store_item=store_item, order=order)

    if not created:
        order_item.quantity += 1
        order_item.save()
    else:

        order_item.quantity = 1
        order_item.save()

    store_item.quantity -= 1
    store_item.save()

    return redirect('index')


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def remove_from_cart_index(request, store_item_id):
    store_item = get_object_or_404(StoreItem, pk=store_item_id)

    order = get_object_or_404(Order, user=request.user, is_completed=False)
    order_item = get_object_or_404(OrderItem, store_item=store_item, order=order)

    if order_item.quantity > 0:
        if order_item.quantity == 1:
            order_item.delete()
            if order.order_items.count() == 0:
                order.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        store_item.quantity += 1
        store_item.save()
    return redirect('index')


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def add_to_cart(request, order_item_id):
    order_item = get_object_or_404(OrderItem, pk=order_item_id)
    store_item = order_item.store_item

    if store_item.quantity > 0:
        order_item.quantity += 1
        order_item.save()
        store_item.quantity -= 1
        store_item.save()
    return redirect('cart')


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def remove_from_cart(request, order_item_id):
    order_item = get_object_or_404(OrderItem, pk=order_item_id)
    store_item = order_item.store_item
    order = order_item.order

    if order_item.quantity > 0:
        if order_item.quantity == 1:
            order_item.delete()
            if order.order_items.count() == 0:
                order.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        store_item.quantity += 1
        store_item.save()
    return redirect('cart')


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def buy(request):
    order = Order.objects.get(user=request.user, is_completed=False)
    if order is None:
        return redirect('index')

    order.is_completed = True
    order.save()

    return redirect('index')


@csrf_protect
def log_in(request):
    if request.user.is_authenticated:
        log_out(request)
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Wrong username or password")
    return render(request, 'log_in.html', context={'form': login_form})


@login_required(login_url='login', redirect_field_name='continue')
def log_out(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(initial=model_to_dict(request.user))

    elif request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

    else:
        form = SettingsForm()
    return render(request, 'settings.html', context={'form': form})


@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        log_out(request)

    if request.method == 'GET':
        profile_form = RegisterForm()
    if request.method == 'POST':
        profile_form = RegisterForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save()
            if profile:
                login(request, profile)
                return redirect(reverse('index'))
            else:
                profile_form.add_error(field=None, error="Profile saving error")
    return render(request, 'signup.html', context={'form': profile_form})


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def cart(request):
    current_order = Order.objects.filter(Q(user=request.user) & Q(is_completed=False)).first()
    order_items = OrderItem.objects.filter(order=current_order)

    return render(request, 'cart.html',
                  {'order_items': order_items})


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def orders(request):
    items = Order.objects.all()

    return render(request, 'orders.html',
                  {'orders': items})
