import os
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from tqdm import tqdm

from diffdrr.data import read
from diffdrr.drr import DRR
from diffdrr.visualization import plot_drr

sns.set_context("talk")

def create_drr(input_folder, output_folder, patient_id=None):
    """
    Tạo ảnh DRR từ dữ liệu DICOM
    
    Args:
        input_folder: Thư mục chứa dữ liệu bệnh nhân LIDC-IDRI
        output_folder: Thư mục lưu ảnh DRR
        patient_id: ID của bệnh nhân cần xử lý (nếu None thì xử lý tất cả)
    """
    # Đảm bảo thư mục đầu ra tồn tại
    os.makedirs(output_folder, exist_ok=True)
    
    # Lấy danh sách bệnh nhân cần xử lý
    patient_folders = []
    if patient_id:
        # Nếu chỉ định ID bệnh nhân cụ thể
        patient_path = os.path.join(input_folder, patient_id)
        if os.path.isdir(patient_path):
            patient_folders = [patient_path]
        else:
            raise ValueError(f"Không tìm thấy thư mục của bệnh nhân: {patient_id}")
    else:
        # Xử lý tất cả bệnh nhân
        for folder in os.listdir(input_folder):
            if folder.startswith("LIDC-IDRI-") and os.path.isdir(os.path.join(input_folder, folder)):
                patient_folders.append(os.path.join(input_folder, folder))
    
    # Khởi tạo thiết bị xử lý (GPU nếu có)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Sử dụng thiết bị: {device}")
    
    # Xử lý từng bệnh nhân
    for patient_folder in tqdm(patient_folders, desc="Xử lý bệnh nhân"):
        patient_id = os.path.basename(patient_folder)
        
        try:
            # Tìm thư mục lớn nhất chứa dữ liệu DICOM
            from get_largest_dicom_folder import get_largest_subfolder
            dicom_folder = get_largest_subfolder(patient_folder)
            
            if not dicom_folder:
                print(f"Không tìm thấy thư mục DICOM cho bệnh nhân {patient_id}")
                continue
                
            # Đọc dữ liệu CT và lấy thông tin về gốc và khoảng cách trong tọa độ thế giới
            subject = read(dicom_folder, labelmap=None, labels=None, orientation="AP", bone_attenuation_multiplier=1.0)
            
            # Khởi tạo module DRR để tạo X-quang giả lập
            drr = DRR(
                subject,     # Đối tượng lưu trữ khối CT, gốc và khoảng cách voxel
                sdd=1020.0,  # Khoảng cách nguồn-đến-máy dò (tức là tiêu cự)
                height=200,  # Chiều cao hình ảnh (nếu chiều rộng không được cung cấp, DRR được tạo ra là hình vuông)
                delx=2.0,    # Khoảng cách pixel (đơn vị mm)
            ).to(device)
            
            # Tạo ảnh DRR với góc và tịnh tiến cố định
            rotations = torch.tensor([[0.0, 0.0, 0.0]], device=device)
            translations = torch.tensor([[0.0, 850.0, 0.0]], device=device)
            img = drr(rotations, translations, parameterization="euler_angles", convention="ZXY")
            
            # Lưu ảnh DRR
            plt.figure(figsize=(10, 10))
            plot_drr(img, ticks=False)
            file_path = os.path.join(output_folder, f"{patient_id}.png")
            plt.savefig(file_path)
            plt.close()
            print(f"Đã tạo DRR cho bệnh nhân {patient_id}")
            
        except Exception as e:
            print(f"Lỗi khi xử lý bệnh nhân {patient_id}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo ảnh DRR từ dữ liệu DICOM")
    parser.add_argument("--input", type=str, default="../filtered_dataset",
                        help="Thư mục chứa dữ liệu bệnh nhân")
    parser.add_argument("--output", type=str, default="./images",
                        help="Thư mục lưu ảnh DRR")
    parser.add_argument("--patient", type=str, default=None,
                        help="ID bệnh nhân cần xử lý (nếu không chỉ định thì xử lý tất cả)")
    
    args = parser.parse_args()
    create_drr(args.input, args.output, args.patient) 