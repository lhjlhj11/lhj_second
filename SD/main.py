import os
from model import save_image
from read_config import read_yaml, read_json
import time

yaml_file = os.path.join(os.getcwd(), f"account.yaml")
dict_config = read_yaml(yaml_file)
my_secret_id = dict_config['tencent_cloud']['my_secret_id']
my_secret_key = dict_config['tencent_cloud']['my_secret_key']
my_region = dict_config['tencent_cloud']['my_region']
my_bucket_name = dict_config['tencent_cloud']['my_bucket_name']

restored_image_file = os.path.join(os.getcwd(), "restored_images")
output_file = []
timestamp = int(time.time())
for image in os.listdir(restored_image_file):
    timestamp += 1
    restored_image_local_file = os.path.join(os.getcwd(), "restored_images", image)
    print(restored_image_local_file)
    image_cloud_file = save_image(secret_id=my_secret_id, secret_key=my_secret_key, region=my_region,
                                  bucket_name=my_bucket_name, local_path=restored_image_local_file,
                                  time_stamp=timestamp)
    output_file.append(image_cloud_file)
print(output_file)
# restored_image_file = os.path.join(os.getcwd(), "restored_images")
# for image in os.listdir(restored_image_file):
#     print(image)
