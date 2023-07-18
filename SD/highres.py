import subprocess
import os



def restore_image(input_file, output_file):
    current_file = os.getcwd()
    command = f"python inference_gfpgan.py -i {input_file} -o {output_file} -v 1.3 -s 2"
    command_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), "GFPGAN")
    os.chdir(command_path)
    subprocess.run(command, capture_output=True, text=True)
    os.chdir(current_file)

# 使用GFPGAN修复图片，提高清晰度
if __name__ == "__main__":
    # current_file = os.getcwd()
    # print(current_file)
    # output_file = os.path.join(os.getcwd(), "outputs")
    # command = f"python inference_gfpgan.py -i inputs/genji -o {output_file} -v 1.3 -s 2"
    # command_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), "GFPGAN")
    # os.chdir(command_path)
    # subprocess.run(command, capture_output=True, text=True)
    # os.chdir(current_file)
    # print(os.getcwd())
    input_file = os.path.join(os.getcwd(), "images")
    output_file = os.path.join(os.getcwd(), "restored_images")
    restore_image(input_file, output_file)


