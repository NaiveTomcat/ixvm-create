#!/usr/bin/env python3.9

import os
import json

metadata_temp = ''
userdata_temp = ''

virt_inst_temp = 'virt-install --name {vmname} --memory 1024 --noreboot --os-variant short-id=debian11 --cloud-init user-data="{userdata_path}",meta-data="{metadata_path}" --disk size=10,backing_store="/home/tomdang/virtimage/debian-11-generic.qcow2" --graphics vnc --network bridge=bridge0 --autostart'

# Information Input

print('Current VM List:')
os.system('virsh list --all')

asn = input('VM Owner ASN: AS')
ident = input('Enter VM Identify ID (1-254): ')

vm_name = f'ixvm_{ident}_AS{asn}'

username = input('Enter username of the client: ')
sshkey = input('Enter ssh pubkey of the client: ')


# Create metadata and userdata

with open('meta-data.template') as f:
    metadata_temp = f.read()

with open('user-data.template') as f:
    userdata_temp = f.read()

metadata = metadata_temp.format(net=ident, iid=f'AS{asn}', hostname=f'AS{asn}')
userdata = userdata_temp.format(username=username, sshkey=sshkey)

dirname = f'{ident}_AS{asn}'
os.mkdir(dirname)
with open(f'{dirname}/metadata','w') as f:
    f.write(metadata)
with open(f'{dirname}/userdata','w') as f:
    f.write(userdata)
cwd = os.getcwd()


# Install VM

virt_inst = virt_inst_temp.format(vmname=vm_name,userdata_path=f'{cwd}/{dirname}/userdata',metadata_path=f'{cwd}/{dirname}/metadata')

print(f'Installing VM: {virt_inst}')
os.system(virt_inst)


output_stream = os.popen(f'./get_vm_ll.sh {asn}')
ipv6ll = output_stream.read().strip()

# Create IXP data

membersdata = {}

with open('ixdata/members.json') as f:
    membersdata = json.load(f)

membersdata["members"].append({"ASN": int(asn), "VMID": vm_name, "ipv4": f"192.168.2.{ident}", "ipv6": ipv6ll})

with open('ixdata/members.json', 'w') as f:
    json.dump(membersdata, f, indent=4)


# TODO: Create bird rs config


# Finish

print('Done')
