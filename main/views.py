from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from .forms import ContactForm
from .models import Product, CartItem
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from django.shortcuts import render



def home(request):
    selected_brands = request.GET.getlist('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    query = request.GET.get('q')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'products': products,
        'brands': Product.objects.values_list('brand', flat=True).distinct(),
        'selected_brands': selected_brands,
        'query': query or "",
        'min_price': min_price or "",
        'max_price': max_price or "",
    }
    return render(request, 'home.html', context)


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login_user')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Неверное имя пользователя или пароль'})

    return render(request, 'login.html')


# Страница коллекций
def collections(request):
    products = Product.objects.all()
    return render(request, 'collections.html', {"products": products})


# Страница о нас
def about(request):
    return render(request, 'about.html')


# Страница личный кабинет
from django.contrib.auth.decorators import login_required
from .models import Favorite

@login_required
def account(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('item')
    return render(request, 'account.html', {
        'favorites': favorites,
        'user': request.user,
    })


def checkout_view(request):
    # Тут можно логика оформления заказа
    return render(request, 'checkout.html')


def contact(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'success': success})





@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')


# views.py




@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Favorite.objects.get_or_create(user=request.user, item=product)
    return redirect('account')

# views.py
from django.shortcuts import render
from .models import Favorite

def account_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('item')
    return render(request, 'collections.html', {
        'user': request.user,
        'favorites': favorites,
    })

@login_required
@require_POST
def delete_favorite(request, id):
    try:
        favorite = Favorite.objects.get(id=id, user=request.user)
        favorite.delete()
    except Favorite.DoesNotExist:
        raise Http404("Избранный товар не найден.")
    return redirect('account')







from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal, InvalidOperation
from .models import Order, OrderItem

@csrf_exempt
def submit_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            address = data.get('address')
            cart = data.get('cart', [])

            # Создаем заказ
            order = Order.objects.create(name=name, email=email, address=address)

            # Создаем позиции заказа
            for item in cart:
                product_name = item.get('name', '')
                price_str = str(item.get('price', '0')).replace('₽', '').strip()
                try:
                    price = Decimal(price_str)
                except InvalidOperation:
                    price = Decimal('0.00')

                OrderItem.objects.create(order=order, product_name=product_name, price=price)

            return JsonResponse({'message': 'Заказ успешно оформлен!'}, status=201)
        except Exception as e:
            print('Ошибка при создании заказа:', e)  # Вывод ошибки в консоль для отладки
            return JsonResponse({'message': f'Ошибка: {str(e)}'}, status=400)

    return JsonResponse({'message': 'Метод не поддерживается'}, status=405)





def blocked_view(request):
    return render(request, 'blocked.html')



import hashlib
import hmac
import time
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest

User = get_user_model()

def telegram_auth(request):
    data = request.GET.dict()


    required_fields = ['id', 'first_name', 'auth_date', 'hash']
    if not all(field in data for field in required_fields):
        return HttpResponseBadRequest("Отсутствуют необходимые данные")


    check_hash = data.pop('hash')
    auth_data_check = '\n'.join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, auth_data_check.encode(), hashlib.sha256).hexdigest()

    if hmac_hash != check_hash:
        return HttpResponseBadRequest("Ошибка проверки подписи")


    auth_date = int(data.get('auth_date'))
    if time.time() - auth_date > 86400:
        return HttpResponseBadRequest("Время авторизации истекло")

    telegram_id = data.get('id')
    first_name = data.get('first_name')
    last_name = data.get('last_name', '')
    username = data.get('username', '')


    try:
        user = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=f"tg_{telegram_id}",
            first_name=first_name,
            last_name=last_name,
            telegram_id=telegram_id,
        )


    login(request, user)


    return redirect('home')
