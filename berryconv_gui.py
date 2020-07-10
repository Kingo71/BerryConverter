from tkinter import *
from tkinter import filedialog
import subprocess
import re

root = Tk()
root.title("Berry Converter")
root.resizable(False, False)

spath = ""
dpath = ""

def openFile():
    sc.delete(0, END)
    converted.delete(0, END)
    rep = filedialog.askopenfilename(
        parent=root,
        initialdir='~/',
        filetypes=[("IMG", "*.img")])
    spath = rep
    dirpath = rep.split('/')
    imgname = dirpath[-1]
    imgsplit = imgname.split('.')
    sc.insert(0, spath)
    dpath = spath[0:spath.rfind('.')] + "_bb.img"
    converted.insert(0, dpath) 

def convertpath():
    rep = filedialog.askdirectory(
        parent=root,
        initialdir='~/')
    dirpath = converted.get().split('/')
    imgname = dirpath[-1]
    converted.delete(0,END)
    converted.insert(0, rep + "/" + imgname) 

def rcommand(param):
    process = subprocess.Popen(param, 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    
    
    while True:
        output = process.stdout.readline()
        if output != "":
            return_string = output.strip()
            console.insert(INSERT,output.strip() + "\n")
        
        console.see("end")
        root.update()
    
        return_code = process.poll()
        
        if return_code is not None:
            
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                if  len(output) > 0:
                    console.insert(INSERT, output.strip() + "\n")
                    console.see("end")
                    root.update()
                    
            return return_code
            


def convert():
    console.config(state="normal")
    console.delete(1.0, END)
    convert.config(state="disabled")
    map_part_command = (rcommand(["sudo", "kpartx", "-av",  sc.get()]))
    map_part = console.get("2.0","2.end").split()[2]
    rcode = rcommand(["sudo", "mount", "/dev/mapper/" + map_part.strip() ,"/mnt"])
    console.insert(INSERT,"Mapping partitions...\n")
    console.see("end")
    root.update()
    rcode = rcommand(["sudo", "sed", "-i",  r"s/^\/dev\/mmcblk/#\0/g",  "/mnt/etc/fstab"])
    rcode = rcommand(["sudo", "sed", "-i", r"s/^PARTUUID/#\0/g", "/mnt/etc/fstab"])
    rcode = rcommand(["sudo", "rm", "-f", "/mnt/etc/console-setup/cached_UTF-8_del.kmap.gz"])
    rcode = rcommand(["sudo", "rm", "-f", "/mnt/etc/systemd/system/multi-user.target.wants/apply_noobs_os_config.service"])
    rcode = rcommand(["sudo", "rm", "-f", "/mnt/etc/systemd/system/multi-user.target.wants/raspberrypi-net-mods.service"])
    rcode = rcommand(["sudo", "rm", "-f", "/mnt/etc/rc3.d/S01resize2fs_once"])
    console.insert(INSERT,"Converting image...\n")
    console.see("end")
    root.update()
    rcode = rcommand(["sudo", "mksquashfs", "/mnt", converted.get(), "-comp", "lzo", "-e", "lib/modules"])
    rcode = rcommand(["sudo", "umount", "/mnt"])
    rcode = rcommand(["sudo", "kpartx", "-d",  sc.get()])
    console.insert(INSERT,"\n Conversion completed\n")
    console.insert(INSERT,"Converted img in:" + converted.get())
    console.see("end")
    console.config(state="disabled")
    convert.config(state="normal")


sourcebrowse = Button(root, text="Source IMG", width=15, command=openFile).grid(row=0, column=0, padx=10, pady=5)
sc = Entry(root, width=60)
sc.grid(row=0, column=1, padx=25)
convertedbrowse = Button(root, text="Converted IMG", width=15, command=convertpath).grid(row=1, column=0, padx=10)
converted = Entry(root, text= "converted.img", width=60)
converted.grid(row=1, column=1, padx=20)

scrollbar = Scrollbar(root, width=25)
scrollbar.grid(row=2, column=2, padx= 20, sticky=N+S)

console = Text(root, height=20, yscrollcommand= scrollbar.set, state="disabled")
console.grid(row=2, pady=5, padx=5, columnspan=2)
scrollbar.config(command=console.yview)

convert = Button(root, text = "Convert", command=convert, width=15)
convert.grid(columnspan=2, pady=5)



root.mainloop()
