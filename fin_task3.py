
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

img_path = "python/OCR_register_account/test/combo.jpg"
img = Image.open(img_path)
text = pytesseract.image_to_string(img, lang='eng').split('\n')

x = {}
x['dish'] = {}
is_dish = False

for i in text:
    if i == "" or i[0] == " ":
        continue
    comp = i.split(' ')
    if comp[0] == "Name:":
        name = ""
        for j in range(1, len(comp)):
            name += (comp[j] + " ")
        name = name[:-1]
        x['alias'] = name
    if comp[0] == "Email:":
        x['email'] = comp[1]
    if comp[0] == "Total":
        is_dish = False
    if comp[0] == "Shop:":
        shop_name = ""
        for j in range(1, len(comp)):
            shop_name += (comp[j] + " ")
        shop_name = shop_name[:-1]
        x['shop name'] = shop_name
    if comp[0] == "Total":
        x['balance'] = comp[1]
    if comp[0] == "Email:":
        is_name = False
    if is_dish:
        if len(comp) == 2:
                dish = comp[0]
                price = comp[1]
        if len(comp) > 2:
            dish = ""
            for j in range(len(comp)-1):
                dish += (comp[j] + " ")
            dish = dish[:-1]
        price = comp[len(comp)-1]
        x['dish'].update({dish:price})
    if comp[0] == "Description":
        is_dish = True

print(x)