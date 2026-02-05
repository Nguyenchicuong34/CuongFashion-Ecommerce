from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from .models import Product, Review, SearchHistory, Category
from .forms import ReviewForm
from .recommendation import get_recommendations

# --- 1. TRANG CHỦ
def product_list(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__name__icontains=category_slug)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        # Lưu lịch sử tìm kiếm
        if request.user.is_authenticated:
            SearchHistory.objects.create(query=query, user=request.user)
        else:
            SearchHistory.objects.create(query=query)

    top_keywords = SearchHistory.objects.values('query').annotate(count=Count('query')).order_by('-count')[:5]

    return render(request, 'store/product_list.html', {
        'products': products,
        'query': query,
        'top_keywords': top_keywords,
        'current_category': category_slug
    })

# --- 2. CHI TIẾT SẢN PHẨM ---
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()

    reviews = product.reviews.all().order_by('-created_at')
    recommendations = get_recommendations(product.id)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'recommendations': recommendations,
        'reviews': reviews,
        'form': form
    })

# --- 3. MUA NGAY (Hàm bạn đang bị thiếu/lỗi) ---
def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Logic xử lý khi bấm "Đặt hàng ngay"
        # Ở đây tạm thời trả về trang thành công
        return render(request, 'store/success.html')

    return render(request, 'store/buy_now.html', {
        'product': product
    })

# --- 4. GIỎ HÀNG ---
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0
    for pk, quantity in cart.items():
        try:
            product = Product.objects.get(pk=pk)
            total = product.price * quantity
            total_price += total
            products.append({'product': product, 'quantity': quantity, 'total': total})
        except Product.DoesNotExist:
            continue

    return render(request, 'store/cart.html', {
        'cart_items': products,
        'total_price': total_price
    })

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart_detail')

def checkout(request):
    if request.method == 'POST':
        if 'cart' in request.session:
            del request.session['cart']
        return render(request, 'store/success.html')
        
    cart = request.session.get('cart', {})
    total_price = 0
    cart_items = []
    for pk, quantity in cart.items():
        try:
            p = Product.objects.get(pk=pk)
            total_price += p.price * quantity
            cart_items.append({'product': p, 'quantity': quantity})
        except Product.DoesNotExist:
            continue

    return render(request, 'store/checkout.html', {
        'total_price': total_price,
        'cart_items': cart_items
    })