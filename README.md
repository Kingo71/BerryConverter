# BerryConverter

Berryboot image conversion script, berryboot converter.

Prerequisites:

A regular Linux desktop computer that has **kpartx** and **mksquashfs** installed.

Setup

copy berryboot_conv.sh in a folder of your choice togheter with the Raspberry image file.
Change the script permission to executable with:

>`chmod 755 berryboot_conv.sh`

Usage:

>`./berryboot_conv.sh <name_image_to_convert> <name_converted_image>`

Example:

> `./berryboot_conv.sh raspios.img raspios_berry.img`
  
The converted image file can be copied to a USB stick and then choosen to be installed in berryboot.
The converted image can be used also in a local network repository.

# BerryConverter GUI  (Beta)

Prerequisites:

A regular Linux desktop computer that has **kpartx** and **mksquashfs** installed along with **Python3**


`Setup`

Copy the file berryconv_gui.py in a folder of your choice, open a terminal in the same location and lunch it as below:

`python3 berryconv_gui.py`

1. Use the button "Source IMG" to select the source image to be converted
2. Use the button "Converted IMG" to select the destination folder and img file name (default is the source name + "_bb")
3. Click on "Convert"to start the conversion, the sudo password will be requested in the opened terminal.
4. wait for the process to finish.






