from django.shortcuts import render, redirect
from pyexpat.errors import messages

from .models import Product
from .forms import RegisterForm
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




from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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
    return render(request, 'collections.html')

def about(request):
    return render(request, 'about.html')
