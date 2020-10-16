# TuringPi K3S Cluster Setup HybriotOS
[![Actions Status](https://github.com/cSDes1gn/blade-k3s/workflows/yaml-lint/badge.svg)](https://github.com/cSDes1gn/blade-k3s/actions) [![Actions Status](https://github.com/cSDes1gn/blade-k3s/workflows/shellcheck/badge.svg)](https://github.com/cSDes1gn/blade-k3s/actions)

![img](img/tp.jpeg) ![img](img/logo_tr.png)![img](img/k3s.png) 

Modified: 2020-10

## Navigation
1. [Setup](#Setup)
2. [Quick Start](#Quickstart)
3. [Node Management](#node-management)

## Quickstart


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
12. Unmount the disk and remove the compute module from the SO-DIMM slot
```bash
diskutil unmountDisk /dev/disk2
```
13. Repeat for remaining compute modules.

### Notes on Reflashing
In order to make the compute module discoverable to your computer the TuringPi must be power cycled with the slave usb flash port jumper set and the compute module in the master SO-DIMM slot.You can run `lsusb` to check just to be sure the device is discoverable. The device will appear as `BCM27XX`

```bash
 % lsusb | grep BCM27
...
Bus 020 Device 000: ID 0a5c:2764 Broadcom Corp. BCM2710 Boot
...
```

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

### Ansible
We will use `ansible` playbooks to manage our cluster:
```bash
brew install ansible
```

Clone the `k3s-ansible` repository by rancher and create a copy of the sample directory but name it your own:
```bash
git clone https://github.com/rancher/k3s-ansible.git
cp -R inventory/sample inventory/cluster-name
```
Edit the `host.ini` and specify your device master and nodes by their hostnames or IP addresses (I found IPs worked better)
```ini
[master]
192.168.2.20

[node]
192.168.2.22
192.168.2.21
192.168.2.23
...

[k3s_cluster:children]
master
node
```

Finally edit the `group_vars/all.yaml` by changing the `ansible_user` field to the user name you gave to your nodes (in my case I chose `hypriot`):
```yaml
---
k3s_version: v1.17.5+k3s1
ansible_user: hypriot
systemd_dir: /etc/systemd/system
master_ip: "{{ hostvars[groups['master'][0]]['ansible_host'] | default(groups['master'][0]) }}"
extra_server_args: ""
extra_agent_args: ""
```

We are now ready to run the ansible playbook to install kubernetes on our cluster:
```bash
ansible-playbook site.yml -i inventory/my-cluster/hosts.ini -vv
```

### Kubectl
Now that k3s is running on the cluster we want to be able to control the cluster. This is done using `kubectl`. First we need to copy the kube config file from the master node to our device:
```bash
scp hypriot@master.local:~/.kube/config ~/Documents/Cluster/.kube/blade-config
```

Next install kubectl using `homebrew`:
```bash
brew install kubectl
```

To verify the k3s install across all nodes run the kubectl test on our client config file:
```bash
 % export KUBECONFIG=~/Documents/Cluster/.kube/blade-config
 % kubectl version
```
This command should identify a client and a server :
```
Client Version: version.Info{Major:"1", Minor:"19", GitVersion:"v1.19.2", GitCommit:"f5743093fd1c663cb0cbc89748f730662345d44d", GitTreeState:"clean", BuildDate:"2020-09-16T21:51:49Z", GoVersion:"go1.15.2", Compiler:"gc", Platform:"darwin/amd64"}
Server Version: version.Info{Major:"1", Minor:"17", GitVersion:"v1.17.5+k3s1", GitCommit:"58ebdb2a2ec5318ca40649eb7bd31679cb679f71", GitTreeState:"clean", BuildDate:"2020-05-06T23:42:31Z", GoVersion:"go1.13.8", Compiler:"gc", Platform:"linux/arm"}
```

Now you can check the status of the cluster by running:
```bash
 % kubectl get nodes
NAME      STATUS   ROLES    AGE    VERSION
master    Ready    master   15h    v1.17.5+k3s1
slave-2   Ready    <none>   131m   v1.17.5+k3s1
slave-3   Ready    <none>   131m   v1.17.5+k3s1
slave-1   Ready    <none>   131m   v1.17.5+k3s1
```
