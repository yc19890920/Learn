import pytesseract
from PIL import Image
import os
import cv2
BASE_DIR = os.path.realpath(os.path.split(__file__)[0])
IMG_DIR = os.path.join(BASE_DIR, "tmp")

captcha_img = os.path.join(IMG_DIR, "captcha_85ad68ca-5d3e-11ea-a423-005056c00008.png")

print(captcha_img)


from PIL import Image
import pytesseract
from utils.utils import log, LoginError, login_required, get_qq_captcha_code

# tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class Languages:
  CHS = 'chi_sim'
  ENG = 'eng'

images=Image.open(captcha_img)
print(images.size)
text=pytesseract.image_to_string(images)
print(text)

# # 使用pytesseract对英文进行识别，lang参数可省略
# s = pytesseract.image_to_string(
#     Image.open(captcha_img), lang=Languages.ENG
# )
# print(s, len(s))
#
# rs, verify_code = get_qq_captcha_code(captcha_img)
# print(rs, verify_code)
