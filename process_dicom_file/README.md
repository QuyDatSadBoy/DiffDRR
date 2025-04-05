# DiffDRR - Tạo ảnh DRR từ dữ liệu DICOM

Dự án này sử dụng thư viện DiffDRR để tạo ảnh X-quang số hóa (Digitally Reconstructed Radiograph - DRR) từ dữ liệu CT (DICOM) của bộ dữ liệu LIDC-IDRI.

## Cấu trúc thư mục

```
process_dicom_file/
├── requirements.txt           # Danh sách thư viện cần thiết
├── kaggle_setup.py            # Script cài đặt môi trường trên Kaggle
├── kaggle_create_drr.py       # Script tạo ảnh DRR từ dữ liệu DICOM
├── kaggle_crop_drr.py         # Script cắt ảnh DRR
├── test_single_patient.py     # Script xử lý một bệnh nhân duy nhất
├── kaggle_notebook.ipynb      # Notebook Kaggle để thực thi trực quan
└── README.md                  # Tệp này
```

## Cài đặt trên Kaggle

1. Tạo một Notebook mới trên Kaggle
2. Upload các file trong thư mục `process_dicom_file`
3. Thêm bộ dữ liệu LIDC-IDRI đã lọc (được yêu cầu trong Dataset hoặc upload thủ công)
4. Chạy file Notebook `kaggle_notebook.ipynb` hoặc các script Python riêng lẻ

## Sử dụng

### Cài đặt môi trường

```python
python kaggle_setup.py
```

### Xử lý một bệnh nhân duy nhất

```python
python test_single_patient.py --patient LIDC-IDRI-0072 --input /path/to/filtered_dataset
```

hoặc chỉ cần ID số:

```python
python test_single_patient.py --patient 0072 --input /path/to/filtered_dataset
```

### Tạo ảnh DRR cho nhiều bệnh nhân

```python
python kaggle_create_drr.py --input /path/to/filtered_dataset --output ./images
```

### Cắt ảnh DRR

```python
python kaggle_crop_drr.py --input ./images --output ./images_cropped
```

## Cấu trúc dữ liệu

Dự án này giả định cấu trúc dữ liệu như sau:

```
filtered_dataset/
├── LIDC-IDRI-0072/
│   └── ...
├── LIDC-IDRI-0141/
│   └── ...
├── LIDC-IDRI-0146/
│   └── ...
└── ...
```

Mỗi thư mục bệnh nhân chứa dữ liệu DICOM của họ. Script `get_largest_subfolder.py` được sử dụng để tìm thư mục DICOM lớn nhất cho mỗi bệnh nhân.

## Điều chỉnh tham số

Các tham số của DRR có thể được điều chỉnh trong file `kaggle_create_drr.py`:

```python
drr = DRR(
    subject,     # Đối tượng lưu trữ khối CT, gốc và khoảng cách voxel
    sdd=1020.0,  # Khoảng cách nguồn-đến-máy dò (tiêu cự)
    height=200,  # Chiều cao hình ảnh
    delx=2.0,    # Khoảng cách pixel (mm)
).to(device)
```

Các tham số cắt ảnh có thể được điều chỉnh trong file `kaggle_crop_drr.py`: 