import requests
from read_config import read_yaml
import os
import base64

yaml_file = os.path.join(os.getcwd(), "account.yaml")
dict_config = read_yaml(yaml_file)
API_KEY = dict_config['image_definition_enhance']['API_KEY']
SECRET_KEY = dict_config['image_definition_enhance']['SECRET_KEY']

def get_access_token():
    request_url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    access_token = str(requests.post(request_url, params=params).json().get("access_token"))
    return access_token

def image_definition_enhance(image_file):
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance"
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())
    payload = {"image": img}
    access_token = get_access_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.post(request_url, headers=headers, data=payload)
    output = response.json()
    return output



if __name__ == "__main__":
    image_file = os.path.join(os.getcwd(), "1.png")
    response = image_definition_enhance(image_file)
    images = response['image']
    with open("1.jpg", 'wb') as f:
        data = base64.b64decode(images)
        f.write(data)




