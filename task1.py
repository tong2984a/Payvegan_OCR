import requests
from PIL import Image
import pytesseract
import sys

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

img_path = "python/OCR_register_account/test/form1.png"
img = Image.open(img_path)
text = pytesseract.image_to_string(img, lang='eng').split('\n')
x = {}
y = {}

for i in text:
    comp = i.split(' ')
    if comp[0] == "Username":
        x['alias'] = comp[len(comp)-1]
        y['alias'] = comp[len(comp)-1]
    if comp[0] == "Contact":
        x['contact'] = comp[len(comp)-1]
y['alias'] = "wowim fine"
y['balance'] = "0.000123484592"
url = 'https://ancient-eyrie-93473.herokuapp.com/users'
resp = requests.get(url).json()
for j in resp:
    if j['alias'] == y['alias']:
        sys.exit("Alias same, no need to create account")
res = requests.post(url, json=y)
print(res.status_code)