# start import
import numpy as np
import cv2 as cv
import pytesseract
import requests

from PIL import Image, ImageEnhance
from skimage.filters import threshold_local
# end import

# start function declaration
def opencv_resize(image, ratio):
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv.resize(image, dim, interpolation = cv.INTER_AREA)

def approximate_contour(contour):
    peri = cv.arcLength(contour, True)
    return cv.approxPolyDP(contour, 0.032 * peri, True)

def get_receipt_contour(contours):    
    for c in contours:
        approx = approximate_contour(c)
        if len(approx) == 4:
            return approx

def contour_to_rect(contour):
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def wrap_perspective(img, rect):
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))    # compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv.getPerspectiveTransform(rect, dst)
    return cv.warpPerspective(img, M, (maxWidth, maxHeight))

def img_process(img):
    text = pytesseract.image_to_string(img, lang='eng+chi_tra').split('\n')
    print(text)
    x = {}
    x['dish'] = {}
    is_dish = False
    for i in text:
        if i == "" or i[0] == " ":
            continue
        for char in i:
            if char == ';':
                char = ':'
        comp = i.split(' ')
        if comp[0][:4] == "Name":
            name = ""
            for j in range(1, len(comp)):
                name += (comp[j] + " ")
            name = name[:-1]
            x['alias'] = name
        if comp[0][:5] == "Email":
            email = ""
            for j in range(1, len(comp)):
                email += (comp[j])
                if j == len(comp)-1:
                    break
                email += "."
            x['email'] = email
        if comp[0][:4] == "Shop":
            shop_name = ""
            for j in range(1, len(comp)):
                shop_name += (comp[j] + " ")
            shop_name = shop_name[:-1]
            x['shop name'] = shop_name
        if comp[0][:5] == "Total":
            is_dish = False
            if len(comp) > 1:
                x['balance'] = comp[1]
        if is_dish:
            dish = ""
            for j in range(len(comp)-1):
                dish += (comp[j] + " ")
            dish = dish[:-1]
            price = comp[len(comp)-1]
            x['dish'].update({dish:price})
        if comp[0][:11] == "Description":
            is_dish = True
    return x

def norm_img_process(filedir, img_name):
    img_dir = filedir+img_name
    img = cv.imread(img_dir)
    resize_ratio = 500 / img.shape[0]
    resize = opencv_resize(img, resize_ratio)
    cv.imwrite(filedir+"resize.jpg", resize)

    gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
    cv.imwrite(filedir+"gray.jpg", gray)

    blur = cv.GaussianBlur(gray, (3,3), 0)
    cv.imwrite(filedir+"blur.jpg", blur)

    rectKernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
    dilate = cv.dilate(blur, rectKernel)
    cv.imwrite(filedir+"dilate.jpg", dilate)

    edge = cv.Canny(dilate, 30, 150)
    cv.imwrite(filedir+"edge.jpg", edge)

    contours, hierarchy = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour = cv.drawContours(gray.copy(), contours, -1, (0, 255, 0), 2, cv.LINE_AA)
    cv.imwrite(filedir+"contours.jpg", contour)

    largest_contours = sorted(contours, key=cv.contourArea, reverse=True)[:5]
    image_with_largest_contours = cv.drawContours(contour, largest_contours, -1, (0,255,0), 3)
    cv.imwrite(filedir+"largest_contour.jpg", image_with_largest_contours)

    receipt_contour = get_receipt_contour(largest_contours)
    image_with_receipt_contour = cv.drawContours(image_with_largest_contours, [receipt_contour], -1, (0, 255, 0), 2)
    cv.imwrite(filedir+"receipt_contour.jpg", image_with_receipt_contour)

    scan = wrap_perspective(gray.copy(), contour_to_rect(receipt_contour))
    cv.imwrite(filedir+"scan.jpg", scan)
    
    contrast = Image.open(filedir+"scan.jpg")
    contrast = ImageEnhance.Contrast(contrast).enhance(3.1)
    contrast.save(filedir+"contrast.jpg")
    
    result = cv.imread(filedir+"contrast.jpg")
    obj = img_process(result)
    print(obj)
# end function declaration

# start code
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    filedir = "python/payvegan_cases/case4b/pic/"
    source = "target.jpg"
    cap = cv.VideoCapture(2, cv.CAP_DSHOW)
    if not cap.isOpened():
        print("Can't open camera")
        exit()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame")
            break
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('s'):
            cv.imwrite(filedir+source, frame)
            break
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break

    norm_img_process(filedir, source)
# end code