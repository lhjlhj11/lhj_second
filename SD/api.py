import os
import time
from flask import Flask, request
from model import txt2img, img2img, decode_image, select_checkpoint, encode_image, generate_image_file_path, save_image
from baiduapi import get_standard_image, removebg
from changeface import change_face
from read_config import read_yaml, read_json
from highres import restore_image

app = Flask(__name__)

prompt_json_file = os.path.join(os.getcwd(), f"prompt.json")
img2imgpayload_orgin_data = read_json(prompt_json_file)
img2imgpayload_orgin = img2imgpayload_orgin_data['img2img_payload_2']

yaml_file = os.path.join(os.getcwd(), f"account.yaml")
dict_config = read_yaml(yaml_file)
my_secret_id = dict_config['tencent_cloud']['my_secret_id']
my_secret_key = dict_config['tencent_cloud']['my_secret_key']
my_region = dict_config['tencent_cloud']['my_region']
my_bucket_name = dict_config['tencent_cloud']['my_bucket_name']

@app.route("/portrait", methods=["POST"])
def painting():
    command = request.form.get("command")
    if command == "txt2img":
        response = txt2img()
        timestamp = int(time.time())
        image_file = decode_image(response, timestamp)
        return image_file
    elif command == "img2img":
        print("----begin----")
        # get image
        image = request.files.get("images")
        input_timestamp = int(time.time())
        image.save(f"./input/input_image_{input_timestamp}.png")
        input_file_name = f"input/input_image_{input_timestamp}.png"
        input_file = os.path.join(os.getcwd(), input_file_name)

        #change to white background
        get_standard_image(input_file)
        removebg(input_file)

        # remove existing images in the output files
        output_file = os.path.join(os.getcwd(), "images")
        restored_image_file = os.path.join(os.getcwd(), "restored_images")
        for image in os.listdir(output_file):
            existing = image.split(".")[-1]
            if existing in ["jpg", "jpeg", "png"]:
                os.remove(os.path.join(output_file, image))

        for image in os.listdir(restored_image_file):
            existing = image.split(".")[-1]
            if existing in ["jpg", "jpeg", "png"]:
                os.remove(os.path.join(restored_image_file, image))

        # encode image
        input_image = encode_image(input_file)
        output_file = []

        for payload in img2imgpayload_orgin:
            images = []
            images.append(input_image)
            img2imgpayload = payload
            img2imgpayload["init_images"] = images

            # setdefault函数有问题，需要直接赋值
            # img2imgpayload.setdefault("init_images", images)
            # img2imgpayload["alwayson_scripts"]["controlnet"]["args"][0].setdefault("input_images", images[0])
            # print(img2imgpayload["alwayson_scripts"]["controlnet"]["args"][0])
            # img2imgpayload["alwayson_scripts"]["controlnet"]["args"][1].setdefault("input_images", images[0])

            # post to SD
            response = img2img(img2imgpayload)

            # local image
            sd_images_timestamp = int(time.time())
            image_local_file = decode_image(response, sd_images_timestamp)

            # change face
            source_image = input_file.split(".")[0]
            result_image = image_local_file.split(".")[0]
            change_face(source_image, result_image, sd_images_timestamp)

            # qcloud image
            # image_cloud_file = save_image(secret_id=my_secret_id, secret_key=my_secret_key, region=my_region,
            #                               bucket_name=my_bucket_name, local_path=image_local_file, time_stamp=timestamp)
            # output_file.append(image_cloud_file)

        # restore images
        restored_input_file = os.path.join(os.getcwd(), "images")
        restored_output_file = os.path.join(os.getcwd(), "restored_images")
        restore_image(restored_input_file, restored_output_file)

        # qcloud image(为什么传重复，只传了三张上去) 解决办法：time.time()的问题，可能是因为读取时间比较慢
        qcloud_time_stamp = int(time.time())
        for image in os.listdir(restored_image_file):
            qcloud_time_stamp += 1
            restored_image_local_file = os.path.join(os.getcwd(), "restored_images", image)
            image_cloud_file = save_image(secret_id=my_secret_id, secret_key=my_secret_key, region=my_region,
                                          bucket_name=my_bucket_name, local_path=restored_image_local_file, time_stamp=qcloud_time_stamp)
            output_file.append(image_cloud_file)

        output = {
            "code": 200,
            "data": output_file,
            "msg": ''
        }
        print("----finish----")
        return output

if __name__ == "__main__":
    app.run(debug=False, host='172.16.10.116')

