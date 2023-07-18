from PIL import Image

# 打开图像并获取宽高
image = Image.open("long-resize.jpg")
width, height = image.size

# 计算裁剪区域
if width > height:
    left = (width - height) / 2
    top = 0
    right = left + height
    bottom = height
else:
    top = (height - width) / 2
    left = 0
    bottom = top + width
    right = width

# 裁剪图像并调整大小
image = image.crop((left, top, right, bottom))
image = image.resize((512, 512), Image.LANCZOS)

# 保存修改后的图像
image.save("example_512x512.png")

