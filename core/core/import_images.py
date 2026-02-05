import os
import django
import random

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Product

# 1. Đường dẫn đến thư mục ảnh bạn vừa tạo
# os.getcwd() lấy thư mục hiện tại của dự án
img_folder = os.path.join(os.getcwd(), 'media', 'products')

# Kiểm tra xem thư mục có thật không
if not os.path.exists(img_folder):
    print(f"Lỗi: Không tìm thấy thư mục tại {img_folder}")
    exit()

# 2. Lấy danh sách tên file ảnh (sp2.jpg, sp3.jpg...)
image_files = sorted([f for f in os.listdir(img_folder) if f.endswith(('.jpg', '.png', '.jpeg'))])

if not image_files:
    print("Thư mục media/products đang trống! Bạn kiểm tra lại xem đã copy ảnh vào chưa nhé.")
    exit()

print(f"✅ Đã tìm thấy {len(image_files)} ảnh (Ví dụ: {image_files[0]}). Đang tiến hành gắn vào sản phẩm...")

# 3. Lấy danh sách sản phẩm và gắn ảnh
products = Product.objects.all()

for i, product in enumerate(products):
    if i < len(image_files):
        # Lấy ảnh theo thứ tự
        img_name = image_files[i]
        
        # Lưu đường dẫn vào CSDL (Dạng: products/sp2.jpg)
        product.image = f"products/{img_name}"
        product.save()
        print(f"  -> Đã gắn ảnh '{img_name}' cho: {product.name}")
    else:
        # Nếu sản phẩm nhiều hơn ảnh, dùng lại ảnh ngẫu nhiên để không bị trống
        random_img = random.choice(image_files)
        product.image = f"products/{random_img}"
        product.save()

print("\nHOÀN TẤT! 30 sản phẩm đã có ảnh đẹp.")