# 🏋️ Phân Tích Dữ Liệu Fitness & Nutrition

> Dự án phân tích dữ liệu luyện tập thể dục và dinh dưỡng từ Kaggle sử dụng Python với lập trình hướng đối tượng (OOP)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 1. Giới Thiệu Đề Tài và Mục Tiêu

### 🎯 Mục Tiêu Dự Án
Dự án này nhằm phân tích và trực quan hóa dữ liệu về hoạt động luyện tập thể dục, dinh dưỡng và các chỉ số sức khỏe của người dùng. Thông qua việc xử lý và phân tích dữ liệu, dự án cung cấp:

- ✅ **Phân tích hiệu suất tập luyện**: So sánh các loại bài tập (Cardio, HIIT, Strength, Yoga)
- ✅ **Tương quan các chỉ số**: Tìm mối liên hệ giữa BPM, BMI, thời gian tập và calories tiêu hao
- ✅ **Phân tích theo nhân khẩu học**: So sánh hiệu suất theo giới tính, độ tuổi
- ✅ **Trực quan hóa dữ liệu**: Tạo dashboard thông tin dễ hiểu với biểu đồ chuyên nghiệp

### 📊 Dataset
- **Nguồn**: [Kaggle - Workout, Nutrition and Health Metrics Dataset](https://www.kaggle.com/datasets/zeesolver/final-dataset)
- **Kích thước**: 20,000 mẫu dữ liệu
- **Số features**: 54 cột (42 số, 12 phân loại)
- **Nội dung**: Thông tin về workout (loại, thời gian, cường độ), chỉ số sinh học (tuổi, cân nặng, chiều cao, BPM), dinh dưỡng

---

## 🛠️ 2. Phương Pháp và Cách Thực Hiện

### 📋 Các Bước Xử Lý Dữ Liệu

#### **Bước 1: Thu Thập Dữ Liệu**
- Tải dataset tự động từ Kaggle sử dụng `kagglehub`
- Backup dữ liệu gốc vào `raw_data.csv`

#### **Bước 2: Làm Sạch Dữ Liệu**
- Xử lý missing values: median cho số, mode cho phân loại
- Loại bỏ duplicates
- Chuẩn hóa kiểu dữ liệu
- Xử lý outliers bằng phương pháp IQR (Interquartile Range)

#### **Bước 3: Feature Engineering**
Tạo 3 features mới:
- `Age_Group`: Phân nhóm tuổi (18-25, 26-35, 36-45, 46-55, 55+)
- `Session_Duration_Minutes`: Chuyển đổi giờ sang phút
- `Calories_Burned_Per_Minute`: Cường độ tập = Calories / Duration

**Lưu ý**: Dataset đã có sẵn cột `BMI` (Body Mass Index), nên không cần tính toán lại.

#### **Bước 4: Phân Tích Dữ Liệu**
- Tính toán correlation matrix
- Phân tích theo nhóm (groupby): workout type, gender, age group
- Tính thống kê mô tả (mean, median, std, min, max)

#### **Bước 5: Trực Quan Hóa**
Tạo 2 dashboard chính:
- **Summary Dashboard**: 4 biểu đồ tổng quan
- **Fitness Insights Dashboard**: 3 biểu đồ chuyên sâu

### 💻 Yêu Cầu Cài Đặt

#### **1. Yêu Cầu Hệ Thống**
- Python 3.8 trở lên
- 4GB RAM trở lên
- 500MB dung lượng trống

#### **2. Cài Đặt Thư Viện**

```bash
# Clone repository
git clone https://github.com/Azunetrangia/Fitness-Nutrition-Analysis.git
cd Fitness-Nutrition-Analysis

# Tạo virtual environment (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

**File requirements.txt:**
```
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
kagglehub>=0.2.0
scikit-learn>=1.3.0
```

#### **3. Cấu Hình Kaggle API**

Để tải dataset tự động, cần cấu hình Kaggle API:

1. Đăng nhập [Kaggle](https://www.kaggle.com)
2. Vào **Account** → **Create New API Token**
3. Download file `kaggle.json`
4. Đặt file vào:
   - Linux/Mac: `~/.kaggle/kaggle.json`
   - Windows: `C:\Users\<username>\.kaggle\kaggle.json`
5. Chmod (Linux/Mac only): `chmod 600 ~/.kaggle/kaggle.json`

#### **4. Chạy Chương Trình**

```bash
python fitness_nutrition_analysis.py
```

Chương trình sẽ:
- ⏬ Tải dataset từ Kaggle (lần đầu tiên)
- 🧹 Làm sạch và xử lý dữ liệu
- 📊 Tạo các biểu đồ phân tích
- 💾 Lưu kết quả vào folder `final_output/`

### 📚 Thư Viện Sử Dụng

| Thư Viện | Phiên Bản | Mục Đích |
|----------|-----------|----------|
| **numpy** | ≥1.24.0 | Tính toán số học, xử lý mảng |
| **pandas** | ≥2.0.0 | Xử lý và phân tích dữ liệu dạng bảng |
| **matplotlib** | ≥3.7.0 | Vẽ biểu đồ cơ bản |
| **seaborn** | ≥0.12.0 | Vẽ biểu đồ thống kê nâng cao |
| **kagglehub** | ≥0.2.0 | Tải dataset từ Kaggle |
| **scikit-learn** | ≥1.3.0 | Xử lý outliers, data preprocessing |

---

## 📈 3. Kết Quả Chạy Chương Trình

### 🖼️ Dashboard Tổng Quan (Summary Dashboard)

![Summary Dashboard](final_output/charts/summary_dashboard.png)

**Bao gồm 4 biểu đồ:**

1️⃣ **Calories Burned Distribution** (Histogram + KDE)
- Phân bố calories tiêu hao của 20,000 mẫu
- Mean: ~1,280 calories
- Phân bố chuẩn, tập trung quanh giá trị trung bình

2️⃣ **Heart Rate vs Calories Burned** (Hexbin Density Map)
- Mối tương quan tích cực giữa BPM và calories
- Vùng mật độ cao: BPM 140-150, Calories 1,000-1,500
- Cho thấy cường độ tập càng cao → tiêu hao calories càng nhiều

3️⃣ **Workout Performance Metrics Comparison** (Grouped Bar Chart)
- So sánh 3 chỉ số: Calories, Duration, BPM
- HIIT có calories cao nhất (~1,630 cal)
- Tất cả workout types có thời gian tương đương (~75 phút)

4️⃣ **Gender × Workout Type Heatmap**
- Hiệu suất theo giới tính và loại workout
- Nam và nữ có calories tương đương trong mọi loại workout
- HIIT là loại workout tiêu hao calories cao nhất cho cả 2 giới

### 🔥 Dashboard Chuyên Sâu (Fitness Insights Dashboard)

![Fitness Insights Dashboard](final_output/charts/fitness_insights_dashboard.png)

**Bao gồm 2 biểu đồ:**

1️⃣ **Workout Intensity Ranking** (Horizontal Bar Chart)
- Cường độ workout tính bằng calories/phút
- **HIIT**: 21.65 cal/min (cao nhất) 
- **Strength**: 17.73 cal/min
- **Cardio**: 15.75 cal/min
- **Yoga**: 11.79 cal/min (thấp nhất)
- Đường median màu xanh đậm cho thấy giá trị trung vị
- Màu gradient từ vàng (thấp) đến xanh lá (cao) giúp dễ nhận biết

2️⃣ **BMI Distribution by Gender** (Violin Plot)
- Phân bố BMI theo giới tính với violin plot
- **Nam**: BMI trung bình 25.0 (khoảng từ 12-50)
- **Nữ**: BMI trung bình 24.9 (khoảng từ 12-50)
- Phân bố hoàn toàn tương đồng giữa 2 giới tính
- Đường ngang trong violin: median (trung vị)
- Độ rộng violin: mật độ dữ liệu ở mỗi mức BMI

### 📊 Các Chỉ Số Chính

| Chỉ Số | Giá Trị |
|--------|---------|
| Tổng số mẫu | 20,000 |
| Số features gốc | 54 |
| Số features sau engineering | 58 |
| Calories trung bình | 1,280 ± 502 cal |
| Thời gian tập trung bình | 75.1 ± 20.8 phút |
| BPM trung bình | 143.7 ± 14.3 |
| Tuổi trung bình | 38.9 ± 12.1 |

### 🔍 Phát Hiện Quan Trọng

#### **Top 3 Yếu Tố Ảnh Hưởng Đến Calories Burned:**
1. **Session_Duration_Minutes**: r = 0.814 (tương quan mạnh nhất)
2. **expected_burn**: r = 0.774
3. **Calories_Burned_Per_Minute**: r = 0.723

#### **Xếp Hạng Cường Độ Workout:**
1. 🥇 **HIIT**: 21.65 cal/min (hiệu quả nhất cho giảm cân)
2. 🥈 **Strength**: 17.73 cal/min
3. 🥉 **Cardio**: 15.75 cal/min
4. **Yoga**: 11.79 cal/min (phù hợp thư giãn)

#### **Phân Tích Giới Tính:**
- Không có sự khác biệt đáng kể giữa nam và nữ
- Female: 1,279.6 ± 496.1 calories
- Male: 1,280.6 ± 508.4 calories

#### **Nhóm Tuổi Hiệu Suất Cao:**
1. 26-35 tuổi: 1,294 calories (cao nhất)
2. 46-55 tuổi: 1,289 calories
3. 18-25 tuổi: 1,282 calories

---

## 💡 4. Nhận Xét và Đánh Giá

### ✅ Ưu Điểm

#### **Về Kỹ Thuật Lập Trình OOP:**
Dự án được thiết kế theo **nguyên lý SOLID** với kiến trúc OOP rõ ràng:

- **Single Responsibility**: Mỗi class đảm nhận một nhiệm vụ cụ thể
  - `Config`: Quản lý cấu hình
  - `DataIngestor`: Xử lý việc tải dữ liệu
  - `DataCleaner`: Làm sạch dữ liệu
  - `FeatureEngineer`: Tạo features mới
  - `DataExplorer`: Phân tích thống kê
  - `Visualizer`: Tạo biểu đồ
  - `OutputManager`: Quản lý output
  - `FitnessDataAnalyzer`: Orchestrator chính

- **Open/Closed**: Code dễ mở rộng mà không cần sửa đổi class gốc
- **Encapsulation**: Dữ liệu và phương thức được đóng gói trong các class
- **Type Hints**: Sử dụng typing để code rõ ràng và dễ maintain

#### **Về Xử Lý Dữ Liệu:**
- ✅ Pipeline hoàn chỉnh từ raw data → insights
- ✅ Xử lý outliers thông minh với IQR method
- ✅ Feature engineering tạo giá trị phân tích cao
- ✅ Correlation analysis phát hiện các yếu tố ảnh hưởng chính

#### **Về Trực Quan Hóa:**
- ✅ Dashboard đẹp, dễ hiểu, phù hợp báo cáo
- ✅ Màu sắc chuyên nghiệp, gradient logic
- ✅ Annotations rõ ràng (giá trị, mean, median)
- ✅ Không bị trùng lặp thông tin giữa các biểu đồ

### 🔄 Hướng Phát Triển

1. **Machine Learning**: Thêm mô hình dự đoán calories
2. **Interactive Dashboard**: Sử dụng Plotly/Dash
3. **API Service**: Tạo REST API cho phân tích real-time
4. **Database Integration**: Lưu trữ dữ liệu trong PostgreSQL/MongoDB
5. **Web Application**: Tạo web app với Flask/FastAPI

---

## ✅ 5. Danh Sách Tác Vụ Python Đã Sử Dụng

### 📦 **Data Structures & Types (4 tác vụ)**
- [x] **Lists & Tuples**: Lưu trữ tên cột, categories
- [x] **Dictionaries**: Lưu grouped statistics, color mapping
- [x] **DataFrames (Pandas)**: Cấu trúc dữ liệu chính
- [x] **Type Hints**: Khai báo kiểu dữ liệu (Dict, Optional, List)

### 📁 **File I/O Operations (4 tác vụ)**
- [x] **CSV Reading**: `pd.read_csv()` - Đọc dataset
- [x] **CSV Writing**: `df.to_csv()` - Lưu processed data
- [x] **Image Saving**: `plt.savefig()` - Lưu biểu đồ PNG
- [x] **Directory Management**: `os.makedirs()`, `os.walk()`

### 🧹 **Data Cleaning & Preprocessing (5 tác vụ)**
- [x] **Missing Value Handling**: `fillna()`, `median()`, `mode()`
- [x] **Duplicate Removal**: `drop_duplicates()`
- [x] **Data Type Conversion**: `astype()`, `pd.to_numeric()`
- [x] **Outlier Capping**: IQR method với `clip()`
- [x] **Data Validation**: Checking null values, data types

### 🔧 **Data Transformation (5 tác vụ)**
- [x] **Feature Engineering**: Tạo BMI, Age_Group, Duration_Minutes
- [x] **Binning**: `pd.cut()` - Phân nhóm tuổi
- [x] **Lambda Functions**: Apply calculations trên từng row
- [x] **String Operations**: Column name manipulation
- [x] **Categorical Encoding**: Convert to category dtype

### 📊 **Statistical Analysis (4 tác vụ)**
- [x] **Descriptive Statistics**: `describe()`, `mean()`, `median()`, `std()`
- [x] **Correlation Analysis**: `corr()` - Ma trận tương quan
- [x] **Groupby Aggregation**: `groupby()`, `agg()`, `pivot_table()`
- [x] **Quantile Calculation**: `quantile()` cho IQR

### 📈 **Data Visualization (6 tác vụ)**
- [x] **Histogram**: `hist()` - Phân bố dữ liệu
- [x] **Density Plot (KDE)**: `plot(kind='kde')` - Đường mật độ
- [x] **Hexbin Plot**: `hexbin()` - Density heatmap
- [x] **Bar Charts**: `bar()`, `barh()` - So sánh categories
- [x] **Heatmap**: `imshow()` - Ma trận màu
- [x] **Violin Plot**: `violinplot()` - Phân bố so sánh

### 🎨 **Plot Customization (5 tác vụ)**
- [x] **Color Mapping**: `plt.cm.RdYlGn()`, `plt.cm.YlOrRd()`
- [x] **Annotations**: `text()` - Thêm labels, giá trị
- [x] **Grid & Style**: `grid()`, `sns.set_style()`
- [x] **Legends**: `legend()` - Chú thích biểu đồ
- [x] **Subplots**: `subplots()`, `add_gridspec()` - Nhiều biểu đồ

### 🏗️ **OOP Implementation (5 tác vụ)**
- [x] **Class Definition**: Định nghĩa 8 classes
- [x] **Dataclass**: `@dataclass` cho Config
- [x] **Constructor (`__init__`)**: Khởi tạo objects
- [x] **Instance Methods**: Methods hoạt động trên instance data
- [x] **Encapsulation**: Private methods với `_method_name()`

### ⚠️ **Error Handling (3 tác vụ)**
- [x] **Try-Except Blocks**: Xử lý lỗi tải data
- [x] **Custom Error Messages**: Thông báo lỗi rõ ràng
- [x] **Warnings Filtering**: `warnings.filterwarnings('ignore')`

### 📦 **Package Management (3 tác vụ)**
- [x] **Import Statements**: Quản lý dependencies
- [x] **Kagglehub API**: `kagglehub.dataset_download()`
- [x] **Backend Configuration**: `matplotlib.use('Agg')`

### 🔄 **Control Flow & Iteration (3 tác vụ)**
- [x] **For Loops**: Iterate qua columns, files, data
- [x] **Conditional Statements**: `if-else` logic
- [x] **List Comprehension**: `[x for x in list if condition]`

### 🎯 **Best Practices (3 tác vụ)**
- [x] **Docstrings**: Documentation cho functions
- [x] **F-strings**: Modern string formatting
- [x] **Constants**: Configuration variables in Config class

**📊 TỔNG CỘNG: 50+ tác vụ Python đã sử dụng**

---

## 📚 6. Tài Liệu Tham Khảo

### 📖 **Dataset**
1. **Kaggle Dataset**: [Workout, Nutrition and Health Metrics](https://www.kaggle.com/datasets/zeesolver/final-dataset)
   - Zeesolver. (2024). Final Dataset - Workout, Nutrition and Health Metrics.

### 📘 **Thư Viện Python**
2. **Pandas Documentation**: https://pandas.pydata.org/docs/
   - McKinney, W. (2023). pandas: powerful Python data analysis toolkit.

3. **Matplotlib Documentation**: https://matplotlib.org/stable/contents.html
   - Hunter, J. D. (2007). Matplotlib: A 2D graphics environment.

4. **Seaborn Documentation**: https://seaborn.pydata.org/
   - Waskom, M. (2021). seaborn: statistical data visualization.

5. **NumPy Documentation**: https://numpy.org/doc/
   - Harris, C. R., et al. (2020). Array programming with NumPy.

6. **Scikit-learn Documentation**: https://scikit-learn.org/stable/
   - Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python.

### 📕 **Lập Trình & Best Practices**
7. **Python OOP Tutorial**: https://realpython.com/python3-object-oriented-programming/
   - Real Python. (2023). Object-Oriented Programming (OOP) in Python 3.

8. **SOLID Principles**: https://realpython.com/solid-principles-python/
   - Real Python. (2023). SOLID Principles: Improve Object-Oriented Design in Python.

9. **PEP 8 Style Guide**: https://pep8.org/
   - van Rossum, G., et al. (2001). PEP 8 – Style Guide for Python Code.

### 📗 **Data Analysis & Visualization**
10. **Data Visualization Best Practices**: 
    - Wilke, C. O. (2019). Fundamentals of Data Visualization. O'Reilly Media.

11. **Exploratory Data Analysis**:
    - Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.

---

## 📧 Liên Hệ

**Author**: Azunetrangia  
**Email**: kg3206722@gmail.com  
**GitHub**: [@Azunetrangia](https://github.com/Azunetrangia)

---

## 📄 License

Dự án này được phân phối dưới giấy phép MIT License. Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

## 🙏 Lời Cảm Ơn

- Cảm ơn [Kaggle](https://www.kaggle.com) và tác giả dataset **Zeesolver** đã cung cấp dữ liệu
- Cảm ơn cộng đồng Python và các nhà phát triển thư viện mã nguồn mở
- Cảm ơn bạn đã quan tâm đến dự án này! ⭐

---

<div align="center">
  <sub>Built with ❤️ using Python & OOP</sub>
</div>
