# start import
import pytesseract
import cv2 as cv
# end import

# start code
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    img = cv.imread("python/payvegan_cases/case3a/pic/1form.png")
    text = pytesseract.image_to_string(img, lang="eng").split('\n')
    print(text)
    x = {}
    isName = False
    isEmail = False
    for comp in text:
        if comp == '' or comp == ' ':
            continue
        if isName == True:
            x['name'] = comp
            isName = False
        if isEmail == True:
            x['email'] = comp[:-1]
            isEmail = False
        word = comp.split(' ')
        if word[0][:4] == "Name":
            isName = True
        if word[0][:5] == "Email":
            isEmail = True
    print(x)
# end code