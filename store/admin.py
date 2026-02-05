from django.contrib import admin
from .models import Category, Product, Review, SearchHistory

# 1. Cấu hình bảng Lịch sử tìm kiếm
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'created_at') # Hiện cột từ khóa, người tìm, thời gian
    list_filter = ('created_at',) # Lọc theo ngày
    search_fields = ('query',)    # Tìm kiếm trong lịch sử

# 2. Cấu hình bảng Đánh giá (Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'rating', 'created_at')
    list_filter = ('rating',)

# 3. Đăng ký các bảng (CHỈ ĐĂNG KÝ 1 LẦN DUY NHẤT Ở ĐÂY)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review, ReviewAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)