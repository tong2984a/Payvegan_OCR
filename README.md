## When a QR code representing user identification is captured using a sequence of QR code frames, the frames are reassembled to act as a fingerprint for a QR code against which later comparisons can be made to detect errors in the data and to check files for integrity. 

1. easyocr 
    - usage 
        - pip install easyocr 
        - python code 
        ```
        import easyocr 
        reader = easyocr.Reader(['th', 'en']) 
        reader.readtext('test.jpg') 
        ```
        - output in list form 
        ![](https://lh3.googleusercontent.com/vhwUAmjUYiYTyHLllJEiUSpig1PA0Pa7_iqrRALhaX9A9hXCMcQEXQeT0ppYM3eYEHjbCciDbQvp7XGOQV-cJn4Ugy4PCUV3uODY0zfuRGEEzA8i1ruXSWs-aZIL-vDkjnxXRQh5=s0)
    - language 
        - Afrikaans (af), Azerbaijani (az), Bosnian (bs), Simplified Chinese (ch_sim),  Traditional Chinese (ch_tra), Czech (cs), Welsh (cy), Danish (da), German (de), English (en), Spanish (es), Estonian (et), French (fr), Irish (ga), Croatian (hr), Hungarian (hu), Indonesian (id), Icelandic (is), Italian (it), Japanese (ja), Korean (ko), Kurdish (ku), Latin (la), Lithuanian (lt), Latvian (lv), Maori (mi), Malay (ms), Maltese (mt), Dutch (nl), Norwegian (no), Polish (pl), Portuguese (pt),Romanian (ro), Slovak (sk), Slovenian (sl), Albanian (sq), Swedish (sv),Swahili (sw), Thai (th), Tagalog (tl), Turkish (tr), Uzbek (uz), Vietnamese (vi) 

2. pytesseract 
    - usage
        - pip install pillow 
        - pip install pytesseract 
        - download the most updated version on (https://digi.bib.uni-mannheim.de/tesseract/)
        - python code
        ```
        from PIL import Image 
        import pytesseract 
        img = Image.open('test1.jpg') 
        text = pytesseract.image_to_string(img, lang='eng') %eng to chi_tra for chinese 
        print(text) 
        ```
        - output as string 
    - language 
        - chi_tra, chi_sim, eng, etc. over 100 languages and has support for characters and symbols 
    - more info on pypi.org and GitHub 
        - (https://github.com/tesseract-ocr/tesseract)
        - (https://pypi.org/project/pytesseract/)
* for compatibility reason, I found a lot of Chi-OCR, but they only supports Chinese language,  which in our case are not useful, as we need to support different languages in Hong Kong  shops, so I omitted them and chose these two for it's wide range support of languages. 
* for updates of QR code readers, I am still trying to do the capture picture function, but in  another form (e.g. pressing 's' key to save the picture), not automation, since I don't know  when is the new QR code is presented, or if we use QR code reader later, I may do a function to  compare the QR code presented now with the database, if new, add to it, if no, just read the QR  code data. Also, the path problem in python is solved, just some minor mistakes made. 
* finished the cropped image when 's' is pressed, but the program will then terminate,  hopefully can find a solution to crop it after pressing 's' button without terminating the  program.

## Image Recognition 
![](https://lh6.googleusercontent.com/xw3nRLAGe8yA1XXT3ZOkqI01poDmr0PaJIsrnJ-N5iGADbU1VYN26Gx1RI34W1j20-YOEt84fz3PyqjT7kPKhSCf_cck8poEee5mlutcSz00VRyXlmBwz7d_v9QAoR-ec4opTN28=s0)
* for updates of image recognition, i can detect qr code.

![](https://lh3.googleusercontent.com/lFCCKgtN4BQVIHlBBJu1NEQLn10uAWZPL9_14mtr8AO4673UINXejsa9s7LASQZ2PZdJGegvw5IIaQIz7wnY8SiGBAiJJuCMy9PFzHT104ccZ_qnMa62P9qnD8jjuHxzDBZ1WLbQ=s0)
* for updates of image recognition, i am working on detection of name and email.

![](https://lh4.googleusercontent.com/Om2xdmlcu_vdzX51FVzUymeMo0n3ubBNkKciAKLTjrHroOGNr2cF2APU2xnXNrXipzm-zu0br4t7grNWb-QUbMiDZxRtXQlWSsRBjq633-yMSzsvM_vgFnWGxbS2ui-6krQ76Hqc=s0)
* for updates of image recognition, i am working on detection of more complex forms. 

![](https://lh5.googleusercontent.com/aBWdTUZr275wM0-Xl0jbuwWtpot2OSQVXWAsDfwThhdG_pJaDzypGevXjHtyRwedzmLQK1I7pomudAf7MuxncDw1m4XmtVaHwkiIWeBP6mumLS3uYd3a0ji8C830BaD8qB0AgmJg=s0)
* for updates of image recognition, i am working on detection of more complex forms. 

![](https://lh6.googleusercontent.com/FZxSeRYVWmdv1jamQs_aFQ63Yo1afYD2H_6EzXZhLGycJjBiSQvvqW6_iLZ9cOEk-GD19qLrFgQSeab8oZjabbw9v9SzJ14ypigBFdiU7yktNxO3VTbZ6OEB8N1WhQdegpFSqGEF=s0)
* for updates of image recognition, i am working on detection of more complex forms.

![](https://lh5.googleusercontent.com/MJuxHW7-dWv0tH7BKLY6uMGX919QPFx9BNZW4AEZnRFYvfVoLwlZK6gaRSVRzJLy0wKJQbw_LwnjQTAeH_WiWpvH15DLQ1pWjSc23o7RDMHJJEAo-bh-N_7JBOTp9yUnvqeC7sA5=s0)
* With period of time stop capturing, e.g. 3 sec 
* The name and email is detected but notice that there's a little space in the email so it's a  failure, the name can be detected tho 
## Proposed Steps to Image Recognition 
1. compile python 
2. detected file path errors, and fixed with absolute paths (need to use relative path for  compatibility) 
3. compilation success 
4. detection success (for photos, it will crop the QR code down, for video/webcam it won't) 
5. for processing, the function detects and gave few scores, choose the highest one  (confidence), and if it is higher than the threshold (0.6), then append to collection 
6. then get the cropped image and show it, also save it in the project directory 
* I installed anaconda, numpy, opencv-python 
numpy in c:\python39\lib\site-packages (1.20.3) 
opencv-python in c:\python39\lib\site-packages (4.5.2.52) 
anaconda download link (https://repo.anaconda.com/archive/Anaconda3-2021.05-Windows-x86_64.exe)

## IoT Programming 
The system consists of a SoC (System on Chip) in the form of an integrated camera with a fully fledged microcontroller and a WiFi module, i.e. ESP32-CAM. In the present case, a computer  that uses a python-based program and OpenCV library to take screenshots from the camera's  IP address and analyze them. 

A Python-based program using the OpenCV library detects QR with YOLO and decodes QR  with Dynamsoft Barcode Reader. YOLO is an extremely fast multi object detection algorithm  which uses convolutional neural network (CNN) to detect and identify objects. The YOLO neural  network has 254 components. In order to run the network you will have to download the pre trained YOLO weight file (237 MB). You can now load the YOLO network model from the  harddisk into OpenCV. The function cv.dnn.blobFromImage(img, scale, size, mean) transforms  the image into a blob. The blob object is given as input to the network. The network divides the  image into regions and predicts bounding boxes and probabilities for each region. These  bounding boxes are weighted by the predicted probabilities. 

The TTGO T-Camera Plus has a microphone (MSM261S4030H0), a temperature, humidity and  atmospheric pressure sensor (BME280), a color TFT screen with a diagonal of 1.3 "and an SD  card reader (up to 16GB) . 

The TTGO T-Camera is equipped with a PIR motion detector (AS312) accessible on the IO33  pin as well as an OLED SSD1306 I2C screen. 

The TTGO T-Journal is directly fitted with an SMA connector. An IPEX connector (uFL) is also  present at the base of the SMA connector. Good idea ! No antenna is engraved on the PCB, so  you must use an external antenna. 

All ESP32 functions are used via ESP-IDF C++ development kit which is based on FreeRTOS.  ESP32-Arduino is the version of the ESP-IDF SDK suitable for the Arduino or PlatformIO IDE.  You will find many projects and examples to get started. This is the preferred solution when 

![](https://lh6.googleusercontent.com/h8WbT-umc9tV8EvaXCu7kQ0-ZEf59EULIXiApRgH-g97wNclZ2m0DtetkTFNq4dFRxFz5Pr3i3Rhg96uJwuQzx_UBgQSsIYRjLmz8BmWmBFDnlF_pTAZASKmPMTu4cCNYuXxLmBP=s0)

The ESP32-CAM camera works in the IP camera mode, connects to a given WiFi network and  then runs its own web server with image sharing. Python-based program using the OpenCV library captures this image, detects the QR code, then detects the QR code sequence. It  determines the position based on the mobile device. 

![](https://lh4.googleusercontent.com/vfVyuzasyYHjO5rQpv9wz9gNEjjNYmAVbWH6DxPXIXJkaFYhX4QF7eoGJVRGtfxgpgL97aaAKRmv1A0HjF-VCEPFeLIEf7LLVeukx2kKTj4gy_sSfGhDR2DK5xL3c-yNb4U9_q4D=s0)

The system should be powered from a stable power source with a voltage of 3.3.  

The ESP32 (unspecified version, probably ESP32-D0WD) has 8MB of PSRAM integrated. The  OmniVision OV3660 module offers a resolution of 2048×1536 pixels and is equipped with a lens  with a field of view of 66.5°.

![](https://lh6.googleusercontent.com/8yOUQvT5G6n3fSX_Q4tBrx6k5PokZtt3wy8GlrFsQsSHQAyy5r2ltW-7A-jDfk3Ad1iUVOmPvBwVlvQ8Pyij4azPtlZUmtDUvRnJhOk1rnc0H75BO3WxSd1xL1xTC3dVUXqRlJWx=s0)  
![](https://lh6.googleusercontent.com/aLM3xZzmp-DioiMNztABPfYrugkhbKH5PTcO0mfvrDb6iKunRpsCJJbKgVA4gwjNPmgn5tp0kLXO-LwWOyifG7zeSpznmYxv0qwhJv3jXbAyU_NyVx6nH1L3CqXjIkZQQzDaKYOJ=s0)

Spectral response between 400nm and 700nm

![](https://lh6.googleusercontent.com/KmMf3Rmpr1F3KZayl7IfxyfDeUrMlEViNYj-Fco4xbZc41Z7HLd8OXA4KcJtLUC0uCpCTJ2_tfPpZead3YFV5l6Ny7zuKpCPDQHkVPNWGy2qSNfAEliqnYSbmHpppkKVGNxdX844=s0)

M5Stack Timer Camera is equipped with a UART / Serial converter (CP2104 controller).  Programming can be done with Arduino code (ESP32-Arduino library), with C++ code (ESP-IDK  4.1 minimum) or in Blockly with UIFlow. 

Timer Camera Pinout 
![](https://lh3.googleusercontent.com/cCknPe3SuvzBUM8KbYbh58V8B00Kas_8AolavAeQka-RG4xUen1RbpDyAvfYJEJXWxBg2tZA8XIjxCYpGRGy7veD93HQqiM1QPsuTagPBgrJKxzhhDPti-5Ozt1lSacRCrLTv3NR=s0)

Proposed Steps to Reconstruct QR Code 
- Crop & Multiple Recognition 
- Process video frames containing QR codes 
- Capture frame-by-frame 
- Remove noise from sample image 
- Narrow down search to only QR code locators 
- Locate the locators 
- Find the alignment pattern square 
- Compensate for perspective warping and extract the code 
- Saves image of the current frame in jpg file 
- To stop duplicate images 
- When everything done, release the capture 
- The file to output the data to. (output is in base64) 
- Convert base64 string to image 

Proposed Steps to QR Code Sequence 
- converts a selected QR Code to base64 
- chunks up the string based on the specified qr_string_size (Note: the larger the chunk  size, the larger the qr_image_size).  
- Convert the chunks into QR Codes and display for playback at a speed specified by the  playback_delay setting. 

Proposed Custom QR Code Reader 
- Browser based written entirely in JavaScript which supports real-time localization and  decoding of various types of barcodes and is also capable of using getUserMedia to get  direct access to the user's camera stream. The code should rely on image-processing  capabilities on recent smartphones for locating and decoding barcodes in real-time. The  implementation features a barcode locator which is capable of finding a barcode-like  pattern in an image resulting in an estimated bounding box including the rotation. The reader should be invariant to scale and rotation so that the barcode is not required to be  aligned with the viewport.

![](https://lh6.googleusercontent.com/CiQaIiNJsFLgKVbyjkO60Obz7mNFFEeIln39mORS1IKVBuiD6ex1J2-jfaptwgbYwbCWVWF-tSqZf7L-69aqFn8YMC3kdBoqjY1PZFlWkezxzCE87haU0wfHBPCbwdxkWEE6A9VV=s0)

Test 1, 23x QR code  
Status : in development  
File : animate.mp4 

Test 2a, 1x QR code  
Condition : processing a downloaded png file without using an external cam Status : 100%  
File : 1xQR.png 

Test 2b, 1x QR code  
Condition : using an external cam?  
Status : not started  
File : 1xQR.png 

Test 3a, Name and Email Only  
Status : not started  
File : form2.png 

Test 3b, handwriting  
Status : not started  
File : form3.png 

Test 4a, combo receipt  
Conditions : Lenovo Legion Y530, indoor, regular paper  
Status : low quality -> overall obscure, human eyes can barely see the words on receipt; low   
mobility -> restricted by its position on the computer, can’t move freely; every computer goes with different internal camera, which ends up different result  
Conditions : Logitech 720p webcam, indoor, regular paper  
Status : low quality -> even more obscure, words are not distinguishable; high  
mobility -> can move freely in range of usb cable; can be used in different computers  
Conditions : DroidCam, indoor, regular paper  
Status : high  
mobility -> can move freely in range of usb cable; high  
quality -> highest in all methods, words are clearly visible; can be attached in different computers with DroidCam Client installed; all data elements can be decoded 100%  
File : combo.png 

Test 4b, combo receipt  
Conditions : outdoor, thermal paper  
Status : Name 100%, Email 100%, Shop 100%, Address 100%, Tele 100%, Total not 100%, QR Code 0%  
File : combo.png 

Test 5. ESP32  
Status : in development  
For methods of using esp32s, since connectivity problem exists, to be specific, appropriate cables are needed, so I can’t find the proper way to program them in this week, but after testing the cameras, which needs delicate extraction of data and high resolution photo outputs.

![](https://lh5.googleusercontent.com/W0I_vPel8wIX2GlM_j_3YffuqzpW4en4X7W8er7IxmebhHXeY9oZdL4XrIs_KnvJNmfqlAH21DlacLzUoZ3iUzYuuFWT-QyY8wYh1ghOkB51OOoVdIiLiduskionBnJ_Rk6nOcKm=s0)

![](https://lh3.googleusercontent.com/E4PZeX6lIYAFSyuFONOu5IEdd53BEbz5LwypbIMcolJjQFQEz8VcNelxIUQY9Icsk0rCZXs0iYf3cyweF7FuyzUAJbYC45JtvWz7zr01cCqLHu4lvgnVyGPvGkHirBWQCwspYnfG=s0)

![](https://lh6.googleusercontent.com/DiBU4RpAxwNb9ls5oTCfzY6nvBqFJuCNgfBKjQBfUupxvIDJH7856faTm0YiFpqqcYxLt4StcDrorO-72Wj2IcCLmNp0UV5trXMyvlaRrLfO17LpPT0asCY5O1djiFxdTN-q_LWB=s0)


![](https://lh5.googleusercontent.com/guHmGRkj6xQpTUb-2JYsJoEFg2LmXfpzbOIA_cfK6aVh9xKyQART_6S19-jjBEXryxQ1hfplSgWwGUZCPMYFnWbhE76LU26JSsMrhTiiDwmVXR8DuI4Hmdb9S5Bw3bu3HjScHWKM=s0)
