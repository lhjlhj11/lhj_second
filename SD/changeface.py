import datetime
import numpy as np
import os
import glob
import cv2
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
import time

def generate_image_file_path(time_stamp):
    filename = f"images/image_{time_stamp}.png"
    file_path = os.path.join(os.getcwd(), filename)
    return file_path

def change_face(source_image_file, result_image_file, timestamp):
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(512, 512))
    swapper_model = os.path.join(os.getcwd(), "model/inswapper_128.onnx")
    swapper = insightface.model_zoo.get_model(swapper_model, download=True, download_zip=True)

    # source_img
    source_img = ins_get_image(source_image_file)
    source_faces = app.get(source_img)
    source_faces = sorted(source_faces, key=lambda x: x.bbox[0])
    source_face = source_faces[0]

    # res_img
    res_img = ins_get_image(result_image_file)
    res_faces = app.get(res_img)
    res_faces = sorted(res_faces, key=lambda x: x.bbox[0])
    # change face
    res_img = swapper.get(res_img, res_faces[0], source_face, paste_back=True)

    image_file = os.getcwd()
    image_name = f"images/image_{timestamp}.png"
    image_file_path = os.path.join(image_file, image_name)
    cv2.imwrite(image_file_path, res_img)


if __name__ == '__main__':
    # app = FaceAnalysis(name='buffalo_l')
    # app.prepare(ctx_id=0, det_size=(640, 640))
    # swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_zip=True)
    #
    # #source_img
    # source_image = f"long"
    # source_file = os.getcwd()
    # source_img_file = os.path.join(source_file, source_image)
    # source_img = ins_get_image(source_img_file)
    # source_faces = app.get(source_img)
    # source_faces = sorted(source_faces, key=lambda x: x.bbox[0])
    # source_face = source_faces[0]
    # #res_img
    # res_image = f"jirounan"
    # res_file = os.getcwd()
    # res_img_file = os.path.join(res_file, res_image)
    # res_img = ins_get_image(res_img_file)
    # res_faces = app.get(res_img)
    # res_faces = sorted(res_faces, key=lambda x: x.bbox[0])
    # #change face
    # res_img = swapper.get(res_img, res_faces[0], source_face, paste_back=True)
    # cv2.imwrite("output.jpg", res_img)

    source_image = f"2_1"
    source_file = os.getcwd()
    source_img_file = os.path.join(source_file, source_image)
    res_image = f"1"
    res_file = os.getcwd()
    res_img_file = os.path.join(res_file, res_image)
    time_stamp = int(time.time())
    change_face(source_img_file, res_img_file, time_stamp)





