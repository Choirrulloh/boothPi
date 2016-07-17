# boothPi
A RaspberryPi driven software to have a photobooth for your wedding (or any other occasion).

## Setup
* Start with a fresh installation of Raspbian
* `sudo apt-get update && sudo apt-get install python-imaging-tk gphoto2`
* `git clone https://github.com/fabianonline/bootPi`
* `cd boothPi`
* `gcc usbreset.c -o usbreset && chmod +x usbreset`
* Disable screensaver and power saving modes.
