from PIL import Image
from pyzbar.pyzbar import decode
import cv2 as cv
import numpy as np
import os

# Start of function declaration
def mse (imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def save_img (img_path, save_path):
    image = cv.imread(img_path)
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
            cv.imwrite(save_path, ROI)
            return ROI
    # cv.imshow('thresh', thresh)
    # cv.imshow('close', close)
    # cv.imshow('image', image)
    # cv.imshow('ROI', ROI)
# End of function declaration

# Start of Code Section
if __name__ == '__main__':
# Video Processing, cutting every different QR code
    cap = cv.VideoCapture("python/payvegan_cases/case1a/animate.mp4")
    frame_filedir = "python/payvegan_cases/case1a/frame/"
    qr_filedir = "python/payvegan_cases/case1a/qr/"
    while cap.isOpened():
        numfile = len(os.listdir(frame_filedir))
        ret, frame = cap.read()
        if not ret:
            print("finished reading the video")
            break;
        gray1 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray1)
        if numfile == 0:
            cv.imwrite(frame_filedir+str(numfile+1)+".jpg", gray1)
        else:
            img_cmp = cv.imread(frame_filedir+str(numfile)+".jpg")
            gray2 = cv.cvtColor(img_cmp, cv.COLOR_BGR2GRAY)
            if (mse(gray1, gray2) < 100):
                continue
            else:
                cv.imwrite(frame_filedir+str(numfile+1)+".jpg", gray1)
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

    # open file to write result
    f = open("python/payvegan_cases/case1a/result.txt", "a")
    # process image to QR code
    for img in os.listdir(frame_filedir):
        img_path = frame_filedir + img
        save_path = qr_filedir + img
        save_img(img_path, save_path)
        data = decode(Image.open(save_path))
        f.write("QR code:\t"+ img)
        f.write("\ndata:\t" + str(data))
        f.write("\n\n")
        
    print("finished cropping and decoding QR code")
    f.close()
# End of Code Section