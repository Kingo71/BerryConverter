#!/usr/bin/env bash

SOURCE=$1
TARGET=$2

if [ -z "$SOURCE" ]; then
    echo "No source file provided"
    exit 1
fi

if [ -z "$TARGET" ]; then
    echo "No target file provided"
    exit 1
fi

MAPPED=`sudo kpartx -av $SOURCE`
COUNT=1

for item in $MAPPED; do
    if [ $COUNT = 12 ]; then
        MAP_PART=$item
    fi
((COUNT++))  
done

sudo mount /dev/mapper/$MAP_PART /mnt
sudo sed -i 's/^\/dev\/mmcblk/#\0/g' /mnt/etc/fstab
sudo sed -i 's/^PARTUUID/#\0/g' /mnt/etc/fstab
sudo rm -f /mnt/etc/console-setup/cached_UTF-8_del.kmap.gz
sudo rm -f /mnt/etc/systemd/system/multi-user.target.wants/apply_noobs_os_config.service
sudo rm -f /mnt/etc/systemd/system/multi-user.target.wants/raspberrypi-net-mods.service
sudo rm -f /mnt/etc/rc3.d/S01resize2fs_once
sudo mksquashfs /mnt $TARGET -comp lzo -e lib/modules
sudo umount /mnt
sudo kpartx -d $SOURCE




