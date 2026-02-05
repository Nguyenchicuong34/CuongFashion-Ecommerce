import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Product, Category

print("Đang dọn dẹp dữ liệu cũ...")
Product.objects.all().delete()
Category.objects.all().delete()

# 1. Tạo 2 Danh mục chính
cat_nam = Category.objects.create(name="Thời trang Nam")
cat_nu = Category.objects.create(name="Thời trang Nữ")

# 2. Tạo sản phẩm Nam
print("Đang tạo sản phẩm Nam...")
names_nam = ['Áo Thun Nam', 'Quần Jeans Nam', 'Áo Khoác Bomber', 'Sơ Mi Nam', 'Quần Short']
for i in range(15):
    name = f"{random.choice(names_nam)} Mẫu {i+1}"
    price = (random.randint(15, 50) * 10000)
    Product.objects.create(name=name, category=cat_nam, price=price, description="Chất liệu cotton cao cấp, nam tính.")

# 3. Tạo sản phẩm Nữ
print("Đang tạo sản phẩm Nữ...")
names_nu = ['Váy Hoa Nhí', 'Đầm Dạ Hội', 'Áo Croptop', 'Chân Váy Ngắn', 'Áo Len Nữ']
for i in range(15):
    name = f"{random.choice(names_nu)} Mẫu {i+1}"
    price = (random.randint(15, 50) * 10000)
    Product.objects.create(name=name, category=cat_nu, price=price, description="Thiết kế dịu dàng, tôn dáng.")

print("✅ Đã tạo xong 15 đồ Nam và 15 đồ Nữ!")