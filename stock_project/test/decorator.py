# -*-coding: utf-8-*-
from PIL import Image
import pytesseract


def test():
    text = pytesseract.image_to_string(Image.open('110.jpg'), lang='chi_sim+eng+chi_tra+osd', config='psm 10')
    return text


if __name__ == '__main__':
    res = test()
    print(res)