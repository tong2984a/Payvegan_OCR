# start import
import pytesseract
import cv2 as cv
import numpy as np
from PIL import Image, ImageEnhance
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

def process_img(filedir, img_name):
    img_dir = filedir+img_name
    img = cv.imread(img_dir)
    resize_ratio = 500 / img.shape[0]
    resize = opencv_resize(img, resize_ratio)
    cv.imwrite(filedir+"resize.jpg", resize)

    contrast = Image.open(filedir+"resize.jpg")
    contrast = ImageEnhance.Contrast(contrast).enhance(2)
    contrast.save(filedir+"contrast.jpg")
    
    img1 = cv.imread(filedir+"contrast.jpg")
    gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    #gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
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
    return scan
# end function declaration

# start code
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    #img = cv.imread("python/payvegan_cases/case3a/pic/2.jpg")
    img = process_img("python/payvegan_cases/case3a/pic/", "12.jpg")
    text = pytesseract.image_to_string(img, lang="eng").split('\n')
    print(text)
    x = {}
    for comp in text:
        if comp == '' or comp == ' ':
            continue
        word = comp.split(' ')
        for i in word:
            if i == ';':
                i = ':'
        if word[0][:4] == "Name":
            name = ""
            for i in range(1, len(word)):
                name += (word[i] + " ")
            x['name'] = name[:-1]
        if word[0][:5] == "Email":
            email = ""
            for i in range(1, len(word)):
                email += (word[i] + ".")
            x['email'] = email[:-1]

    print(x)
# end code