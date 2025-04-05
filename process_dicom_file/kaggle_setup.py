import os
import subprocess
import sys

def setup_environment():
    """
    Cài đặt môi trường và các thư viện cần thiết cho DiffDRR trên Kaggle
    """
    print("Đang cài đặt các thư viện cần thiết...")
    
    # Cài đặt các thư viện từ requirements.txt
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Đảm bảo sử dụng GPU nếu có 
    import torch
    if torch.cuda.is_available():
        print(f"Đã xác nhận GPU khả dụng: {torch.cuda.get_device_name(0)}")
        print(f"Số lượng GPU: {torch.cuda.device_count()}")
    else:
        print("Không tìm thấy GPU! Chương trình sẽ chạy trên CPU.")
    
    # Tạo thư mục lưu kết quả
    os.makedirs("./images", exist_ok=True)
    os.makedirs("./images_cropped", exist_ok=True)
    
    print("Đã hoàn tất thiết lập môi trường!")

if __name__ == "__main__":
    setup_environment() 