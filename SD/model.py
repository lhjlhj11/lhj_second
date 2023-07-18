import requests
import io
import base64
from PIL import Image, PngImagePlugin
import os
import time
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


#stable diffusion api
sd_api = "http://127.0.0.1:7860"

def encode_image(input_file):
    with open(input_file, 'rb') as file:
        image_data = file.read()
    image = base64.b64encode(image_data).decode('utf-8')
    return image

# input_file_name = f"input/input_image.png"
# input_file = os.path.join(os.getcwd(), input_file_name)
# controlnet_image = encode_image(input_file)
# print(controlnet_image)

txt2img_payload = {
    "prompt": "a girl",
    "negative_prompt": "EasyNegative, nsfw, bad-hands-5, paintings, sketches, (worst quality:2), ..., NSFW, child, childish",
    "steps": 28,
    "sampler_name": "DPM++ SDE Karras",
    "width": 512,
    "height": 512,
    "restore_faces": True,
    # "alwayson_scripts": {
    #     "controlnet": {
    #         "args": [
    #             {
    #                 "input_image": controlnet_image,
    #                 "module": "canny",
    #                 "model": "control_sd15_canny [fef5e48e]"
    #             },
    #             {
    #                 "input_image": controlnet_image,
    #                 "module": "lineart_standard",
    #                 "model": "None"
    #             }
    #         ]
    #     }
    # }
}
img2imgpayload = {
    'init_images': [],
    'prompt': "(masterpiece), best quality, boy, (((handsome))), gorgeous, portrait, suit, stage light , godfather , series man, premium lounge , noir",
    'negative_prompt': "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, mustache, EasyNegative , female, girl",
    'steps': 28,
    'sampler_name': "Euler a",
    'denoising_strength': 0.88,
    "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        # "input_image": controlnet_image,
                        "module": "depth_midas",
                        "model": "control_v11f1p_sd15_depth",
                        "weight": 0.5
                    },
                    {
                        # "input_image": controlnet_image,
                        "module": "lineart_standard",
                        "model": "control_v11p_sd15_lineart",
                        "weight": 0.5
                    }
                ]
            }
        }
}



#select checkpoint
option_payload = {
    "sd_model_checkpoint": "anything-v4.5.ckpt",
    "CLIP_stop_at_last_layers": 2
}

#file of images
def generate_image_file_path(time_stamp):
    filename = f"images/image_{time_stamp}.png"
    file_path = os.path.join(os.getcwd(), filename)
    return file_path

#select checkpoint
def select_checkpoint():
    api_url = f"{sd_api}/sdapi/v1/options"
    response = requests.post(api_url, json=option_payload)
# select_checkpoint()

#txt2img
def txt2img():
    api_url = f"{sd_api}/sdapi/v1/txt2img"
    response = requests.post(api_url, json=txt2img_payload)
    r = response.json()
    return r

#img2img
def img2img(img2img_payload):
    api_url = f'{sd_api}/sdapi/v1/img2img'
    response = requests.post(api_url, json=img2img_payload)
    r = response.json()
    return r

#decode_image, return_url, save_image, r is json
def decode_image(r, time_stamp):
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{sd_api}/sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image_file_path = generate_image_file_path(time_stamp)
        image.save(image_file_path, pnginfo=pnginfo)
        return image_file_path

def get_controlnet_inf():
    api_url = f'{sd_api}/controlnet/model_list'
    response = requests.get(api_url)
    print(response.json())
    api_url = f'{sd_api}/controlnet/module_list'
    response = requests.get(api_url)
    print(response.json())

#save image to qcloud, return url, local_path
def save_image(secret_id, secret_key, region, bucket_name, local_path, time_stamp, token=None,):
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
    client = CosS3Client(config)
    key = "images/image_{}.png".format(time_stamp)
    response = client.put_object_from_local_file(
        Bucket=bucket_name,
        LocalFilePath=local_path,
        Key=key
    )
    image_url = client.get_object_url(Bucket=bucket_name, Key=key)
    return image_url



if __name__ == '__main__':
#     #test

#     #txt2img
#     # r = txt2img()
#     # print(r)
#     # file_path = decode_image(r)
#     # print(file_path)

    #img2img
    input_file_name = [f"input/input_image_1689146617.png", f"input/input_image_1689146730.png"]
    # input_file_name = input_file_name[1]
    # input_file = os.path.join(os.getcwd(), input_file_name)
    # input_image = encode_image(input_file)
    # images = []
    # images.append(input_image)

    for files in input_file_name:
        input_file = os.path.join(os.getcwd(), files)
        input_image = encode_image(input_file)
        images = []
        images.append(input_image)
        img2imgpayload = img2imgpayload
        img2imgpayload["init_images"] = images

        #setdefault函数有问题，需要直接赋值
        #img2imgpayload.setdefault("init_images", images)

        r = img2img(img2imgpayload)
        timestamp = int(time.time())
        file_path = decode_image(r, timestamp)

    # img2imgpayload = img2imgpayload1
    # img2imgpayload.setdefault("init_images", images)
    # r = img2img(img2imgpayload)
    # timestamp = int(time.time())
    # file_path = decode_image(r, timestamp)
