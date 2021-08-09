# start import
from PIL import Image
from pyzbar.pyzbar import decode
import cv2 as cv
import numpy as np
import os
# end import

# start function declaration
def save_img (input_path, output_path, img_name):
    image = cv.imread(input_path+img_name)
    original = image.copy()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9,9), 0)
    thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    # Morph close
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    close = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=2)

    # Find contours and filter for QR code
    cnts = cv.findContours(close, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv.boundingRect(approx)
        area = cv.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
            cv.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            ROI = original[y:y+h, x:x+w]
            cv.imwrite(output_path+img_name, ROI)
            return ROI
# end function declaration

# start code
if __name__ == '__main__':
    input_path = "python/payvegan_cases/case2a/input/"
    output_path = "python/payvegan_cases/case2a/output/"
    img_name = "14.jpg"
    save_img(input_path, output_path, img_name)
    f = open("python/payvegan_cases/case2a/result.txt", "a")
    data = decode(Image.open(output_path+img_name))
    f.write("QR code:\t"+output_path+img_name+"\n")
    f.write("data:\t\t"+str(data)+"\n")
    f.write("\n")
    f.close()