import os
import cv2
BASE_DIR = os.path.realpath(os.path.split(__file__)[0])
IMG_DIR = os.path.join(BASE_DIR, "tmp")

loc = {'x': 463, 'y': 444}

image = cv2.imread(
    os.path.join(IMG_DIR, "screenshot_a8f5ff54-5d3c-11ea-8552-005056c00008.png")
)
captcha_img = os.path.join(IMG_DIR, "a.png")

roi = image[int(loc['y']):int(loc['y'])+48, int(loc['x']):int(loc['x'])+130]
cv2.imwrite(captcha_img, roi)