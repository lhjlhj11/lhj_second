import os
import yaml
import json

def read_yaml(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        config = f.read()
    dict_config = yaml.load(config, Loader=yaml.FullLoader)
    return dict_config

def read_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data




