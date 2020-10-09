# K3S Blade Cluster on TuringPi
Modified: 2020-10

## Navigation
1. [Setup](#Setup)
2. [Node Management](#node-management)

## Setup
1. Set the first jumper closest to the micro-usb slave programmer port so that it is on the pin with the small triangle indicator. This sets the pinstate to eMMC flash mode. 
2. Connect micro-usb to computer
3. Insert eMMC compute module into the master SO-DIMM slot
4. Power TuringPi using 12V VDC in or mini-ITX power cable
5. Clone the usbboot scripts from the rasberrypi foundation repository and install `libusb`
```bash
git clone https://github.com/raspberrypi/usbboot.git
brew install libusb
```
6. Make and execute the usbboot script
```bash
cd usbboot/
make;
sudo ./rpiboot
```
7. Identify disk volume and unmount for flashing
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
8. Download the most recent hypriotos image from [Hybriot's download page](https://blog.hypriot.com/downloads/) and move the image to your current working directory
9. Flash the eMMC using `dd`. Install and use `pv` to track progress
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
10. Copy your public ssh key for the nodes user-data configuration file
```bash
cat ~/.ssh/id_rsa.pub
```
11. Using a text editor edit the hostname field to your preference and add an `ssh_authorized_keys` field with your public rsa key as the value:
```bash
vi /Volumes/HypriotOS/user-data
```

```yaml
#cloud-config
# vim: syntax=yaml
#

# Set your hostname here, the manage_etc_hosts will update the hosts file entries as well
hostname: edit your hostname here
manage_etc_hosts: true

# You could modify this for your own user information
users:
  - name: pirate
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
12. Unmount the disk and remove the compute module from the SO-DIMM slot
```bash
diskutil unmountDisk /dev/disk2
```
13. Repeat for remaining compute modules.

## Node Management
Find your ip for your home network:
```bash
 % ifconfig
...
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether 8c:85:90:76:f4:35 
	inet6 fe80::1c1e:71a8:4c56:5a14%en0 prefixlen 64 secured scopeid 0x5 
	inet 192.168.2.11 netmask 0xffffff00 broadcast 192.168.2.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
...
```
Search your ip space for other connnected devices. You can filter by the expected hostnames:
```bash
nmap -sn 192.168.2.1/32 | grep 'master\|slave'
```