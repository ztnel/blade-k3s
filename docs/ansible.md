# Ansible Playbook for k3s Setup

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