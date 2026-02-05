import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Product

print("Đang nâng cấp thông tin sản phẩm...")

materials = ["Cotton 100% cao cấp", "Vải Kaki nhập khẩu", "Jean co giãn 4 chiều", "Lụa tơ tằm nhân tạo"]
origins = ["Việt Nam", "Hàn Quốc", "Thái Lan", "Nhật Bản"]
durability = ["Cao", "Trung bình", "Siêu bền"]

products = Product.objects.all()

for p in products:
    mat = random.choice(materials)
    ori = random.choice(origins)
    dur = random.choice(durability)
    
    # Tạo mô tả chi tiết chuẩn SEO
    new_desc = (
        f"✅ THÔNG TIN CHI TIẾT:\n"
        f"- Chất liệu: {mat}, thấm hút mồ hôi tốt, không bai xù.\n"
        f"- Xuất xứ: {ori}.\n"
        f"- Độ bền: {dur}, cam kết giặt máy thoải mái.\n"
        f"- Phong cách: Trẻ trung, năng động, phù hợp đi làm, đi chơi.\n\n"
        f"⭐ HƯỚNG DẪN BẢO QUẢN:\n"
        f"- Giặt ở nhiệt độ thường.\n"
        f"- Không dùng thuốc tẩy mạnh.\n"
        f"- Phơi ở nơi thoáng mát."
    )
    
    p.description = new_desc
    # Cập nhật lại giá cho lẻ lẻ nhìn cho thật (Ví dụ: 259,000)
    p.price = (random.randint(15, 90) * 10000) + 9000 
    p.save()

print("Đã cập nhật xong! Vào web xem thử nhé.")