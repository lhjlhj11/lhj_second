import requests
import base64
from PIL import Image
import os

sd_api = "http://127.0.0.1:7860"
url = f"{sd_api}/tagger/v1/interrogate"
# # model = 'wd14-convnext-v2'
model = 'wd14-vit-v2-git'
threshold = 0.35

def get_caption(images_file):
    for image in os.listdir(images_file):
        image_file_path = os.path.join(images_file, image)
        with open(image_file_path, 'rb') as f:
            image_data = f.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        data = {
            "image": base64_image,
            "model": model,
            "threshold": threshold
        }
        response = requests.post(url, json=data)
        json_data = response.json()
        # 处理返回的JSON数据
        caption_dict = json_data['caption']
        sorted_items = sorted(caption_dict.items(), key=lambda x: x[1], reverse=True)
        image_caption = ""
        for captions in sorted_items:
            if captions[1] >= 0.34:
                image_caption = image_caption + captions[0] + ','
        text_name = image.split(".")[0]
        with open(f"{images_file}/{text_name}.txt", "w") as f:
            f.write(image_caption)
            f.close()

if __name__ == "__main__":
    images_file = os.path.join(os.getcwd(), "yl_train_data")
    get_caption(images_file)

