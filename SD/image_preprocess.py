import requests
import base64
from collections import OrderedDict
from PIL import Image
import os
import time

def resize(image_file, output_width, output_height):
    image = Image.open(image_file)
    width, height = image.size

    # 计算裁剪区域
    if width > height:
        left = (width - height) / 2
        top = 0
        right = left + height
        bottom = height
    else:
        top = (height - width) / 2
        left = 0
        bottom = top + width
        right = width

    # 裁剪图像并调整大小
    image = image.crop((left, top, right, bottom))
    image = image.resize((output_width, output_height), Image.LANCZOS)

    # 保存修改后的图像
    time_stamp = int(time.time())
    image_save_file = f"image_preprocess"
    save_file = os.getcwd()
    save_file = os.path.join(save_file, image_save_file)
    image.save(f"{save_file}/{time_stamp}.png")


#为一张图片打标签
# def caption_images(image_file):
#
#     #读取文件名
#     image_name = os.path.basename(image_file)
#     image_name = image_name.split('.')[0]
#
#     model = 'wd14-vit-v2-git'
#     threshold = 0.35
#
#     #二进制形式读图片
#     with open(image_file, 'rb') as file:
#         image_data = file.read()
#         base64_image = base64.b64encode(image_data).decode('utf-8')
#
#     #构建请求体的JSON数据
#     data = {
#         "image": base64_image,
#         "model": model,
#         "threshold": threshold
#     }
#
#     # 发送POST请求
#     response = requests.post(caption_url, json=data)
#     # 检查响应状态码
#     if response.status_code == 200:
#         json_data = response.json()
#         # 处理返回的JSON数据
#         caption_dict = json_data['caption']
#         sorted_items = sorted(caption_dict.items(), key=lambda x: x[1], reverse=True)
#         #写标签
#         image_caption = ""
#         for captions in sorted_items:
#             if captions[1] >= 0.34:
#                 image_caption = image_caption + captions[0] + ','
#         with open(f"{image_name}.txt", "w") as file:
#             file.write(image_caption)
#             file.close()
#     else:
#         print('Error:', response.status_code)
#         print('Response body:', response.text)


sd_api = "http://127.0.0.1:7860"
caption_url = f"{sd_api}/tagger/v1/interrogate"
#为一个文件夹的图片打标签
def caption_images(image_file):

    # 遍历文件夹
    image_folder = os.listdir(image_file)
    for image in image_folder:
        file_path = os.path.join(image_file, image)

        # 读取图片名
        image_name = os.path.basename(file_path)
        image_name = image_name.split('.')[0]

        model = 'wd14-vit-v2-git'
        threshold = 0.35

        # 二进制形式读图片
        with open(file_path, 'rb') as f:
            image_data = f.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')

        # 构建请求体的JSON数据
        data = {
            "image": base64_image,
            "model": model,
            "threshold": threshold
        }

        # 发送POST请求
        response = requests.post(caption_url, json=data)
        # 检查响应状态码
        if response.status_code == 200:
            json_data = response.json()
            # 处理返回的JSON数据
            caption_dict = json_data['caption']
            sorted_items = sorted(caption_dict.items(), key=lambda x: x[1], reverse=True)
            # 写标签
            image_caption = ""
            for captions in sorted_items:
                if captions[1] >= 0.34:
                    image_caption = image_caption + captions[0] + ','
            with open(f"{image_file}/{image_name}.txt", "w") as file:
                file.write(image_caption)
                file.close()
        else:
            print('Error:', response.status_code)
            print('Response body:', response.text)

if __name__ == "__main__":

    #输入文件夹名称
    file_name = os.getcwd()
    file_name = os.path.join(file_name, "image_preprocess")

    #遍历文件夹
    caption_images(file_name)






