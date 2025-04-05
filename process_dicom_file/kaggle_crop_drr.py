import os
import argparse
from PIL import Image
from tqdm import tqdm

def crop_images(input_folder, output_folder, patient_id=None):
    """
    Cắt ảnh DRR từ thư mục đầu vào và lưu vào thư mục đầu ra
    
    Args:
        input_folder: Thư mục chứa ảnh DRR
        output_folder: Thư mục lưu ảnh DRR đã cắt
        patient_id: ID bệnh nhân cần xử lý (nếu None thì xử lý tất cả)
    """
    try:
        # Kiểm tra và tạo thư mục đầu ra nếu chưa tồn tại
        os.makedirs(output_folder, exist_ok=True)
        
        if not os.path.exists(input_folder):
            print(f"Thư mục {input_folder} không tồn tại.")
            return
        
        # Lọc danh sách file cần xử lý
        files_to_process = []
        for filename in os.listdir(input_folder):
            if filename.endswith(".png"):
                if patient_id is None or patient_id in filename:
                    files_to_process.append(filename)
        
        # Xử lý cắt ảnh
        for filename in tqdm(files_to_process, desc="Cắt ảnh DRR"):
            file_path = os.path.join(input_folder, filename)
            with Image.open(file_path) as img:
                # Kích thước crop (thay đổi tùy theo ảnh của bạn)
                left = 321
                top = 61
                right = img.width - 294
                bottom = img.height - 54
                
                img_cropped = img.crop((left, top, right, bottom))
                output_path = os.path.join(output_folder, filename)
                img_cropped.save(output_path)
                
        print(f"Đã cắt và lưu {len(files_to_process)} ảnh vào {output_folder}")
        
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cắt ảnh DRR")
    parser.add_argument("--input", type=str, default="./images",
                        help="Thư mục chứa ảnh DRR")
    parser.add_argument("--output", type=str, default="./images_cropped",
                        help="Thư mục lưu ảnh DRR đã cắt")
    parser.add_argument("--patient", type=str, default=None,
                        help="ID bệnh nhân cần xử lý (nếu không chỉ định thì xử lý tất cả)")
    
    args = parser.parse_args()
    crop_images(args.input, args.output, args.patient) 