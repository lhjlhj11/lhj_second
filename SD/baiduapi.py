import os
import requests
import base64
from PIL import Image
from read_config import read_yaml

yaml_file = os.path.join(os.getcwd(), f"account.yaml")
dict_config = read_yaml(yaml_file)
my_client_id = dict_config['baidu_cloud']['my_client_id']
my_client_secret = dict_config['baidu_cloud']['my_client_secret']

def get_access_token(client_id, client_secret):
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    data = {
        'grant_type': 'client_credentials',  # 固定值
        'client_id': client_id,
        'client_secret': client_secret
    }
    res = requests.post(url, data=data)
    res = res.json()
    access_token = res['access_token']
    return access_token

#white background
def fullwhite(png_name):
    im = Image.open(png_name)
    x, y = im.size
    try:
        p = Image.new('RGBA', im.size, (255, 255, 255))        # 使用白色来填充背景,视情况更改
        p.paste(im, (0, 0, x, y), im)
        p.save(png_name)
    except:
        pass

#change background 要求输入格式为png
def removebg(image_file):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg"
    # 二进制方式打开图片文件
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    access_token = get_access_token(my_client_id, my_client_secret)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        res = response.json()["foreground"]
        png_name = image_file.split('.')[0]+".png"
        with open(png_name, "wb") as f:
            data = base64.b64decode(res)
            f.write(data)
        fullwhite(png_name)

def resize_image(image_file, compress_rate= 0.5):
    im = Image.open(image_file)
    w, h = im.size
    im_resize = im.resize((int(w * compress_rate), int(h * compress_rate)))
    resize_w, resieze_h = im_resize.size
    im_resize.save(image_file)
    im.close()

def get_size(image_file):
    size = os.path.getsize(image_file)
    return size / 1024

#resize image
def get_standard_image(image_file):
    size = get_size(image_file)
    while size >= 4000:
        resize_image(image_file, compress_rate=0.9)
        size = get_size(image_file)

if __name__ == '__main__':
    print("---begin---")
    image_path = f"sen2.jpg"
    file_path = os.getcwd()
    image_file_path = os.path.join(file_path, image_path)
    get_standard_image(image_file_path)
    removebg(image_file_path)
    print("---finish---")
















































