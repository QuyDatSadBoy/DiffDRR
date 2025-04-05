import os
import argparse
from kaggle_create_drr import create_drr
from kaggle_crop_drr import crop_images

def process_single_patient(patient_id, input_folder="../filtered_dataset"):
    """
    Xử lý một bệnh nhân duy nhất: tạo DRR và cắt ảnh
    
    Args:
        patient_id: ID của bệnh nhân cần xử lý (ví dụ: LIDC-IDRI-0072)
        input_folder: Thư mục chứa dữ liệu bệnh nhân
    """
    if not patient_id.startswith("LIDC-IDRI-"):
        patient_id = f"LIDC-IDRI-{patient_id}"
    
    print(f"Bắt đầu xử lý bệnh nhân {patient_id}")
    
    # Tạo thư mục đầu ra
    images_folder = "./images"
    cropped_images_folder = "./images_cropped"
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(cropped_images_folder, exist_ok=True)
    
    # Tạo ảnh DRR
    print("Đang tạo ảnh DRR...")
    create_drr(input_folder, images_folder, patient_id)
    
    # Cắt ảnh DRR
    print("Đang cắt ảnh DRR...")
    crop_images(images_folder, cropped_images_folder, patient_id)
    
    print(f"Đã hoàn thành xử lý bệnh nhân {patient_id}")
    print(f"Ảnh DRR gốc: {images_folder}/{patient_id}.png")
    print(f"Ảnh DRR đã cắt: {cropped_images_folder}/{patient_id}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xử lý một bệnh nhân duy nhất")
    parser.add_argument("--patient", type=str, required=True,
                        help="ID bệnh nhân cần xử lý (ví dụ: LIDC-IDRI-0072 hoặc chỉ 0072)")
    parser.add_argument("--input", type=str, default="../filtered_dataset",
                        help="Thư mục chứa dữ liệu bệnh nhân")
    
    args = parser.parse_args()
    process_single_patient(args.patient, args.input) 