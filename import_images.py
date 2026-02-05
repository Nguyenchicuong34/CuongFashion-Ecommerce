import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Product

base_dir = os.path.dirname(os.path.abspath(__file__))

def gan_anh(category_name, folder_name):
    folder_path = os.path.join(base_dir, 'media', folder_name)
    if not os.path.exists(folder_path):
        print(f"⚠️ Chưa có thư mục 'media/{folder_name}'. Hãy tạo và copy ảnh vào!")
        return

    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not images:
        print(f"⚠️ Thư mục '{folder_name}' trống!")
        return

    products = Product.objects.filter(category__name=category_name)
    print(f"🔄 Đang gắn ảnh cho {len(products)} sản phẩm {category_name}...")

    for i, p in enumerate(products):
        img = images[i % len(images)] # Lấy vòng tròn nếu thiếu ảnh
        p.image = f"{folder_name}/{img}" # Lưu đường dẫn: nam/anh1.jpg
        p.save()

# Chạy gắn ảnh cho từng loại
gan_anh("Thời trang Nam", "nam")
gan_anh("Thời trang Nữ", "nu")
print("🎉 HOÀN TẤT GẮN ẢNH!")