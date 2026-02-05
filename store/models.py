from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
    class Meta:
        verbose_name_plural = "Categories" # Chỉnh lại cho đúng chính tả

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    # Thay đổi: Dùng ImageField để upload ảnh thật
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self): return self.name

    # Hàm tạo Link QR thanh toán tự động (VietQR)
    # STK: 000000 (Ví dụ) - Ngân hàng: MBBank (Ví dụ)
    def get_qr_url(self):
        # Cấu trúc: https://img.vietqr.io/image/[BankID]-[AccountNo]-[Template].png?amount=[Price]&addInfo=[Content]
        # Bạn thay 'MB' và '0987654321' bằng Ngân hàng và STK thật của bạn
        return f"https://img.vietqr.io/image/MB-0987654321-compact2.png?amount={int(self.price)}&addInfo=Mua {self.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=50) # Tên người bình luận
    rating = models.IntegerField(default=5)  # Điểm sao (1-5)
    comment = models.TextField()             # Nội dung bình luận
    created_at = models.DateTimeField(auto_now_add=True) # Ngày giờ viết

    def __str__(self):
        return f"{self.author} - {self.product.name}"


class SearchHistory(models.Model):
    query = models.CharField(max_length=255) # Từ khóa khách tìm (Ví dụ: quần jeans)
    created_at = models.DateTimeField(auto_now_add=True) # Thời gian tìm
    
    # Nếu web có đăng nhập thì lưu user, không thì để trống
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Tìm kiếm: {self.query} - lúc {self.created_at.strftime('%d/%m/%Y %H:%M')}"