# Documentation for Manual Setup

1. Clone the usbboot scripts from the rasberrypi foundation repository and install `libusb`
```bash
git clone https://github.com/raspberrypi/usbboot.git
brew install libusb
```
2. Make and execute the usbboot script
```bash
cd usbboot/
make;
sudo ./rpiboot
```
3. Identify disk volume and unmount for flashing
```bash
 % diskutil list
 /dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *251.0 GB   disk0
   1:                        EFI EFI                     314.6 MB   disk0s1
   2:                 Apple_APFS Container disk1         250.7 GB   disk0s2

/dev/disk1 (synthesized):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      APFS Container Scheme -                      +250.7 GB   disk1
                                 Physical Store disk0s2
   1:                APFS Volume Macintosh HD - Data     173.9 GB   disk1s1
   2:                APFS Volume Preboot                 82.4 MB    disk1s2
   3:                APFS Volume Recovery                529.0 MB   disk1s3
   4:                APFS Volume VM                      6.4 GB     disk1s4
   5:                APFS Volume Macintosh HD            11.3 GB    disk1s5

/dev/disk2 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:                                                   *7.8 GB     disk2

 % diskutil unmountDisk /dev/disk2
```
4. Download the most recent hypriotos image from [Hybriot's download page](https://blog.hypriot.com/downloads/) and move the image to your current working directory
5. Flash the eMMC using `dd`. Install and use `pv` to track progress
```bash
brew install pv
```
```bash
 % pv hypriotos-rpi-v1.12.3.img | sudo dd bs=1m of=/dev/rdisk2
1.27GiB 0:03:47 [5.72MiB/s] [===========================================================================================================================>] 100%            
0+20800 records in
0+20800 records out
1363148800 bytes transferred in 227.435230 secs (5993569 bytes/sec)
```
6. Copy your public ssh key for the nodes user-data configuration file
```bash
cat ~/.ssh/id_rsa.pub
```
7. Using a text editor edit the hostname field to your preference and add an `ssh_authorized_keys` field with your public rsa key as the value:
```bash
vi /Volumes/HypriotOS/user-data
```
It is critical that all the nodes have the same name for when we install k3s! This name cannot be modified without reflashing hypriot so be sure to verify the name before flashing
```yaml
#cloud-config
# vim: syntax=yaml
#

# Set your hostname here, the manage_etc_hosts will update the hosts file entries as well
hostname: edit your hostname here
manage_etc_hosts: true

# You could modify this for your own user information
users:
  - name: hypriot
    gecos: "Hypriot Pirate"
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    groups: users,docker,video,input
    plain_text_passwd: hypriot
    lock_passwd: false
    ssh_pwauth: true
    chpasswd: { expire: false }
    ssh_authorized_keys:
      - paste your ssh rsa key here

# # Set the locale of the system
# locale: "en_US.UTF-8"
...
```
8. Unmount the disk and remove the compute module from the SO-DIMM slot
```bash
diskutil unmountDisk /dev/disk2
```
9. Repeat for remaining compute modules.

### Notes on Reflashing
In order to make the compute module discoverable to your computer the TuringPi must be power cycled with the slave usb flash port jumper set and the compute module in the master SO-DIMM slot.You can run `lsusb` to check just to be sure the device is discoverable. The device will appear as `BCM27XX`

```bash
 % lsusb | grep BCM27
...
Bus 020 Device 000: ID 0a5c:2764 Broadcom Corp. BCM2710 Boot
...
```