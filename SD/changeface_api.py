from flask import Flask, request
from changeface import change_face
import time
import os
from read_config import read_yaml
from model import save_image

app = Flask(__name__)

yaml_file = os.path.join(os.getcwd(), f"account.yaml")
dict_config = read_yaml(yaml_file)
my_secret_id = dict_config['tencent_cloud']['my_secret_id']
my_secret_key = dict_config['tencent_cloud']['my_secret_key']
my_region = dict_config['tencent_cloud']['my_region']
my_bucket_name = dict_config['tencent_cloud']['my_bucket_name']

@app.route("/changeface", methods=["POST"])
def changeface():
    source_image = request.files.get("source_image")
    result_image = request.files.get("result_image")
    input_timestamp = int(time.time())

    source_image.save(f"./change_face_input/source_image_{input_timestamp}.png")
    source_file_name = f"change_face_input/source_image_{input_timestamp}.png"
    source_file = os.path.join(os.getcwd(), source_file_name)
    source_file = source_file.split(".")[0]

    result_image.save(f"./change_face_input/result_image_{input_timestamp}.png")
    result_file_name = f"change_face_input/result_image_{input_timestamp}.png"
    result_file = os.path.join(os.getcwd(), result_file_name)
    result_file = result_file.split(".")[0]

    change_face(source_file, result_file, input_timestamp)
    image_local_file = os.path.join(os.getcwd(), f"images/image_{input_timestamp}.png")
    image_cloud_file = save_image(secret_id=my_secret_id, secret_key=my_secret_key, region=my_region,
                                  bucket_name=my_bucket_name, local_path=image_local_file, time_stamp=input_timestamp)
    output = {
        "code": 200,
        "data": image_cloud_file,
        "msg": ''
    }

    return output

if __name__ == "__main__":
    app.run(debug=False, host='172.16.10.116', port=5001)
