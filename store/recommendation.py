# store/recommendation.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Product

def get_recommendations(product_id, num_recommendations=5):
    # 1. Lấy tất cả sản phẩm từ Database
    products = Product.objects.all()
    
    # Chuyển đổi dữ liệu Django QuerySet sang Pandas DataFrame
    df = pd.DataFrame(list(products.values('id', 'name', 'description')))
    
    # Nếu ít sản phẩm quá thì không cần gợi ý
    if len(df) < 2:
        return []

    # 2. Tạo TF-IDF Matrix (Biến đổi văn bản mô tả thành các vector số học)
    # Stop_words='english' loại bỏ các từ vô nghĩa (the, a, an...). 
    # Với tiếng Việt thực tế cần bộ từ điển riêng, ở đây ta dùng cơ bản.
    tfidf = TfidfVectorizer(stop_words='english') 
    
    # Phân tích cột 'description'
    tfidf_matrix = tfidf.fit_transform(df['description'])

    # 3. Tính độ tương đồng Cosine (Cosine Similarity)
    # So sánh các vector với nhau để xem sản phẩm nào giống sản phẩm nào
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # 4. Lấy index của sản phẩm hiện tại trong DataFrame
    try:
        idx = df.index[df['id'] == product_id][0]
    except IndexError:
        return []

    # 5. Lấy điểm tương đồng của sản phẩm này với tất cả sản phẩm khác
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 6. Sắp xếp theo điểm số cao nhất (giống nhất)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 7. Lấy top sản phẩm (bỏ qua chính nó ở vị trí 0)
    sim_scores = sim_scores[1:num_recommendations+1]
    
    # 8. Lấy Product ID của các sản phẩm gợi ý
    product_indices = [i[0] for i in sim_scores]
    recommend_ids = df['id'].iloc[product_indices].tolist()

    # 9. Truy vấn lại database để lấy object Product
    return Product.objects.filter(id__in=recommend_ids)