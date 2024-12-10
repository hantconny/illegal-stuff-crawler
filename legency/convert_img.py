# -*- coding:utf-8 -*-
from PIL import Image
import os


def convert_to_jpg(input_file, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 打开图片
    with Image.open(input_file) as img:
        # 获取文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        # 构造输出文件路径
        output_file = os.path.join(output_dir, f"{base_name}.jpg")

        # 转换为RGB模式（避免PNG的透明通道）
        rgb_image = img.convert("RGB")

        # 保存为JPG
        rgb_image.save(output_file, "JPEG")
        print(f"Converted {input_file} to {output_file}")


# 示例：批量转换某目录下的图片
def batch_convert_to_jpg(input_dir, output_dir):
    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(('.png', '.bmp')):
            input_file = os.path.join(input_dir, file_name)
            convert_to_jpg(input_file, output_dir)


# 使用示例
input_dir = r"C:\Users\Administrator\下载\archive (1)\dataset\training_set\person"  # 输入图片文件夹路径
output_dir = r"C:\Users\Administrator\下载\archive (1)\dataset\training_set\person\jpg"  # 输出文件夹路径

batch_convert_to_jpg(input_dir, output_dir)
