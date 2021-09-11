1. create Raspberry Pi Operating System on SD card
   1. go to https://www.raspberrypi.org/software/, under Install Raspberry Pi OS using
Raspberry Pi Imager, install the suitable imager for your current operating system
   2. run the imager, choose Operating System as RASPBERRY PI OS (32-BIT), Storage as
the designated micro SD card, and write
   3. insert micro SD card to raspberry pi, check display port (usb type-A to HDMI),
keyboard (usb 2.0), mouse (usb 2.0), finally insert power cable (usb type-C), as before
powering up the OS, keyboard and mouse is a must to control the OS
   4. boot with micro SD and setup raspberry pi following instructions given and
personal preference
2. download required dependencies for payvegan cases (in terminal)
   1. sudo apt update
   2. sudo apt full-upgrade
   3. sudo apt-get install atool cmake tesseract-ocr python3 libatlas-base-dev libavformat-dev libavutil-dev libswscale-dev libv4l-dev libglew-dev libgtk2.0-dev libasound2-dev libspeex-dev libplist-dev gtk+-3.0 libappindicator3-dev raspberrypi-kernel-headers android-sdk-platform-tools-common libatlas-doc liblapack-doc libusbmuxd-tools libusbmuxd-dev android-tools-adb android-tools-fastboot

       #### if you see these:
       
       ```
       Err:1 http://raspbian.raspberrypi.org/raspbian buster InRelease
       Temporary failure resolving 'raspbian.raspberrypi.org'
       Err:2 http://archive.raspberrypi.org/debian buster InRelease
       Temporary failure resolving 'archive.raspberrypi.org'
       ```
       
       #### then do these:
       
       ```
       sudo -s
       echo "nameserver 8.8.8.8" >> /etc/resolv.conf
       chmod 644 /etc/resolv.conf
       exit
       ```
   4. pip3 install pytesseract pyzbar numpy opencv-python pillow
   5. pip3 install -U numpy
3. Droidcam Client
   1. <strike>download libjpeg-turbo-2.1.0.tar.gz from https://sourceforge.net/projects/libjpegturbo/files/2.1.0/ in ~/Downloads
   2. mv ~/Downloads/libjpeg-turbo-2.1.0.tar.gz /tmp
   3. cd /tmp
   4. atool -x libjpeg-turbo-2.1.0.tar.gz
   5. cd libjpeg-turbo-2.1.0</strike>
   6. cd /tmp
   7. git clone https://github.com/libjpeg-turbo/libjpeg-turbo.git
   8. cd /tmp/libjpeg-turbo
   9. cmake -G "Unix Makefiles" .
   10. make
   11. sudo make install
   12. cd /tmp
   13. git clone https://github.com/dev47apps/droidcam.git
   14. cd /tmp/droidcam
   15. make droidcam-cli
   16. make droidcam
   17. sudo ./install-client
   18. sudo ./install-sound
   19. sudo ./install-video
   20. sudo ./install-dkms
   21. sudo usermod -aG plugdev $LOGNAME
   22. log out and log in
   23. droidcam
4. Run Program:
   1. cd ~/Desktop/payvegan_cases/
   2. choose desired case (num1-4 a/b)
   3. cd case$(num+a/b)
   4. python3 $(num+a/b).py
