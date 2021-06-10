import requests
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

img_path = "python/OCR_register_account/test/combo.png"
img = Image.open(img_path)
text = pytesseract.image_to_string(img, lang='eng').split('\n')

is_dish = False
is_name = False
x = {} #x is the data needed in task3
y = {} #y is the data needed to update
x['dish'] = {}

for i in text:
    if i == "" or i[0] == " ":
        continue
    comp = i.split(' ')
    if comp[0] == "KEKE":
        is_dish = False
    if comp[0] == "SHOP":
        x['shop name'] = comp[1]
    if comp[0] == "Total":
        x['balance'] = comp[1]
        y['balance'] = comp[1]
    if comp[0] == "Email:":
        is_name = False
    if is_name:
        name = ""
        for j in range(len(comp)):
            name += (comp[j] + " ")
        name = name[:-1]
        x['alias'] = name
        y['alias'] = name
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
    if len(comp) >= 2 and comp[1] == "Name:":
        is_name = True
    if comp[0] == "Description":
        is_dish = True
print(y)

api_url = 'https://ancient-eyrie-93473.herokuapp.com/users'
url = 'https://ancient-eyrie-93473.herokuapp.com/earnings/Tom%20Brady'
resp = requests.get(api_url).json()
is_post = False
for j in resp:
    if j['alias'] == y['alias']:
        result = float(y['balance'])
        params = {"id":j['id']}
        body = {
            "amount": result,
            "currencyCode": "XBT"
        }
        res = requests.post(url, params=params, json=body)
        print(res.status_code)
        is_post = True

if not is_post:
    res = requests.post(api_url, json=y)
    print(res.status_code)

#response = requests.post(url, data=json.dumps(x), headers=)
#print(response.status_code)