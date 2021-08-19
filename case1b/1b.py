import cv2 as cv
from pyzbar.pyzbar import decode
import time

txt_file = "python/payvegan_cases/case1b/result.txt"
cap = cv.VideoCapture(2, cv.CAP_DSHOW)
code_set = []
if not cap.isOpened():
    print("Can't open camera")
    exit()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame")
        break
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        print(code_set)
        f = open(txt_file, "a")
        f.write(time.asctime(time.localtime(time.time())))
        f.write(str(code_set)+"\n")
        f.close()
        exit()
    for code in decode(frame):
        data = code.data.decode('utf-8')
        if data not in code_set:
            print(code.type)
            print(data)
            code_set.append(data)
            print("code added in code set")
            #time.sleep(3)
        elif data in code_set:
            print("code is already added")
            #time.sleep(3)
        else:
            pass
    cv.imshow('frame', frame)
    cv.waitKey(1)