import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Try to import the real Faker package. If it's not installed, provide a
# lightweight fallback implementation that supports the subset of methods
# used in this script (currently only date_time_between).
try:
    from faker import Faker
except ImportError:
    print("Warning: 'faker' package not found. Install it with 'pip install Faker' to use realistic fake data. Falling back to a lightweight implementation.")
    class Faker:
        def __init__(self, locale=None):
            # locale accepted for API compatibility but unused in fallback
            self.locale = locale

        def date_time_between(self, start_date=None, end_date=None):
            # Accept datetime inputs (the way this script calls it).
            # If non-datetime provided, fall back to 1 year range ending now.
            s = start_date if isinstance(start_date, datetime) else datetime.now() - timedelta(days=365)
            e = end_date if isinstance(end_date, datetime) else datetime.now()
            if s > e:
                # swap if user passed in inverted dates
                s, e = e, s
            delta = e - s
            total_seconds = max(delta.total_seconds(), 0)
            rand_sec = random.uniform(0, total_seconds) if total_seconds > 0 else 0
            return s + timedelta(seconds=rand_sec)

# Khởi tạo Faker cho dữ liệu tiếng Việt
fake = Faker('vi_VN')

# --- 1. THIẾT LẬP CÁC THAM SỐ ---
N_TRANSACTIONS = 500  # Số lượng giao dịch
N_CUSTOMERS = 150     # Số lượng khách hàng (để có giao dịch lặp lại)

# Các danh mục giả định cho Techcombank
TRANS_TYPES = ['Ăn uống', 'Mua sắm', 'Di chuyển', 'Thanh toán hóa đơn', 'Giải trí', 'Du lịch', 'Sức khỏe', 'Chuyển khoản', 'Giáo dục']
CHANNELS = ['Mobile App', 'Internet Banking', 'Tại quầy (OTC)', 'ATM', 'POS']
SEGMENTS = ['Standard', 'Gold', 'Priority']
PAYMENT_METHODS = ['Thẻ tín dụng', 'Thẻ ghi nợ', 'Chuyển khoản (App)', 'QR Code']
STATUSES = ['Thành công', 'Thất bại', 'Đang xử lý']
LOCATIONS = ['Hà Nội', 'TP. Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ', 'Bình Dương', 'Đồng Nai', 'Quảng Ninh']
OCCUPATIONS = ['Nhân viên văn phòng', 'Kỹ sư', 'Bác sĩ', 'Giáo viên', 'Sinh viên', 'Giám đốc', 'Kinh doanh tự do', 'Nội trợ', 'Lập trình viên']

# --- 2. TẠO DỮ LIỆU KHÁCH HÀNG (CUSTOMER DIMENSION) ---
# Tạo một bảng khách hàng riêng để đảm bảo tính nhất quán
# (Mỗi CustomerID luôn có cùng Age, Occupation, Segment...)
print(f"Đang tạo {N_CUSTOMERS} khách hàng giả định...")
customer_data = []
customer_ids = [f"TCB{10000 + i}" for i in range(1, N_CUSTOMERS + 1)]

for cid in customer_ids:
    age = np.random.randint(18, 65)
    # Thâm niên (tenure) phải logic với tuổi (không thể 20 tuổi mà thâm niên 10 năm)
    max_tenure = max(1, age - 18)
    tenure = np.random.randint(1, max_tenure + 1)
    occupation = random.choice(OCCUPATIONS)
    
    # Logic gán Phân khúc (Segment)
    # Ưu tiên Priority cho Giám đốc, Kinh doanh, thâm niên lâu
    if (occupation in ['Giám đốc', 'Kinh doanh tự do'] and tenure > 5) or tenure > 10:
        segment = np.random.choice(SEGMENTS, p=[0.1, 0.3, 0.6]) # 60% Priority
    elif tenure > 5:
        segment = np.random.choice(SEGMENTS, p=[0.3, 0.5, 0.2]) # 50% Gold
    else:
        segment = np.random.choice(SEGMENTS, p=[0.7, 0.2, 0.1]) # 70% Standard
        
    customer_data.append({
        'CustomerID': cid,
        'CustomerAge': age,
        'CustomerOccupation': occupation,
        'CustomerSegment': segment,
        'Location': random.choice(LOCATIONS),
        'CustomerTenure': tenure
    })

df_customers = pd.DataFrame(customer_data)

# --- 3. TẠO DỮ LIỆU GIAO DỊCH (TRANSACTION FACT) ---
print(f"Đang tạo {N_TRANSACTIONS} giao dịch giả định...")
transaction_data = []
end_date = datetime.now()
start_date = end_date - timedelta(days=365) # Giao dịch trong 1 năm qua

for _ in range(N_TRANSACTIONS):
    # Chọn ngẫu nhiên một khách hàng từ danh sách
    customer_profile = df_customers.sample(n=1).iloc[0]
    
    trans_type = random.choices(TRANS_TYPES, 
                                weights=[0.2, 0.2, 0.1, 0.15, 0.1, 0.05, 0.05, 0.1, 0.05], k=1)[0]
    
    # Logic về Số tiền (Amount)
    # Số tiền phụ thuộc vào Loại giao dịch và Phân khúc khách hàng
    base_amount = 100000
    if trans_type == 'Ăn uống':
        base_amount = np.random.randint(50000, 2000000)
    elif trans_type == 'Mua sắm':
        base_amount = np.random.randint(200000, 15000000)
    elif trans_type == 'Di chuyển':
        base_amount = np.random.randint(20000, 500000)
    elif trans_type == 'Thanh toán hóa đơn':
        base_amount = np.random.randint(100000, 5000000)
    elif trans_type == 'Du lịch':
        base_amount = np.random.randint(2000000, 50000000)
    elif trans_type == 'Chuyển khoản':
        base_amount = np.random.randint(1000000, 100000000)
    
    # Khách hàng Priority chi tiêu nhiều hơn
    segment_multiplier = 1.0
    if customer_profile['CustomerSegment'] == 'Priority':
        segment_multiplier = np.random.uniform(1.5, 3.0)
    elif customer_profile['CustomerSegment'] == 'Gold':
        segment_multiplier = np.random.uniform(1.0, 1.8)
        
    amount = round((base_amount * segment_multiplier) / 1000) * 1000 # Làm tròn đến hàng nghìn
    
    # Logic về Kênh và Phương thức
    channel = random.choices(CHANNELS, weights=[0.5, 0.15, 0.05, 0.1, 0.2], k=1)[0]
    if channel == 'Mobile App':
        payment_method = random.choice(['Chuyển khoản (App)', 'QR Code', 'Thẻ ghi nợ'])
    elif channel == 'POS':
        payment_method = random.choice(['Thẻ tín dụng', 'Thẻ ghi nợ', 'QR Code'])
    elif channel == 'ATM':
        payment_method = 'Thẻ ghi nợ'
    else:
        payment_method = random.choice(PAYMENT_METHODS)

    transaction_data.append({
        'CustomerID': customer_profile['CustomerID'],
        'TransactionTimestamp': fake.date_time_between(start_date=start_date, end_date=end_date),
        'Amount': amount,
        'TransactionType': trans_type,
        'Channel': channel,
        'PaymentMethod': payment_method,
        'TransactionStatus': random.choices(STATUSES, weights=[0.95, 0.04, 0.01], k=1)[0],
        # Thêm các cột thông tin khách hàng đã tra cứu
        'CustomerAge': customer_profile['CustomerAge'],
        'CustomerOccupation': customer_profile['CustomerOccupation'],
        'CustomerSegment': customer_profile['CustomerSegment'],
        'Location': customer_profile['Location'],
        'CustomerTenure': customer_profile['CustomerTenure']
    })

df_transactions = pd.DataFrame(transaction_data)

# --- 4. HOÀN THIỆN BỘ DỮ LIỆU ---
# Sắp xếp theo thời gian
df_final = df_transactions.sort_values(by='TransactionTimestamp').reset_index(drop=True)

# Thêm TransactionID duy nhất (sau khi đã sắp xếp)
df_final.insert(0, 'TransactionID', [f"TX{1002000 + i}" for i in range(N_TRANSACTIONS)])

# Sắp xếp lại các cột theo đúng thứ tự bạn yêu cầu
columns_ordered = [
    'TransactionID',
    'CustomerID',
    'TransactionTimestamp',
    'Amount',
    'TransactionType',
    'Channel',
    'CustomerAge',
    'CustomerOccupation',
    'CustomerSegment',
    'PaymentMethod',
    'TransactionStatus',
    'Location',
    'CustomerTenure'
]
df_final = df_final[columns_ordered]

# Xuất ra file CSV
output_file = 'techcombank_transactions.csv'
df_final.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n--- HOÀN TẤT ---")
print(f"Đã tạo thành công file '{output_file}' với {len(df_final)} dòng.")
print("Dữ liệu 5 dòng đầu tiên:")
print(df_final.head())