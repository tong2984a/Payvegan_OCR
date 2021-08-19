# start import
from PIL import Image
from pyzbar.pyzbar import decode

import pytesseract
import cv2 as cv
# end import

# start function declaration
def process_img (image):
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
    ROI = None
    for c in cnts:
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv.boundingRect(approx)
        area = cv.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
            cv.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            ROI = original[y:y+h, x:x+w]

    cv.imshow('thresh', thresh)
    cv.imshow('close', close)
    cv.imshow('image', image)
    cv.imshow('ROI', ROI)  
# end function declaration

# start code
if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    filedir = "python/payvegan_cases/case3b/target.jpg"
    cap = cv.VideoCapture(2, cv.CAP_DSHOW)
    if not cap.isOpened():
        print("Can't open camera")
        exit()
    is_cap = False
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame")
            break
        cv.imshow('frame', frame)
        if is_cap == True:
            process_img(frame)
        if cv.waitKey(1) & 0xFF == ord('s'):
            is_cap = True
            continue
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break
# end code