from PIL import Image

img = Image.open("calendar.png").convert(mode='L').point(lambda x: 0 if x<128 else 255, '1')
img.save("calendar.bmp")
