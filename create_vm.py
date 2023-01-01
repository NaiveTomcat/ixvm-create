#!/usr/bin/env python3.9

import os

metadata_temp = ''
userdata_temp = ''

virt_inst_temp = 'virt-install --name {vmname} --memory 1024 --noreboot --os-variant short-id=debian11 --cloud-init user-data="{userdata_path}",meta-data="{metadata_path}" --disk size=10,backing_store="/home/tomdang/virtimage/debian-11-generic.qcow2" --graphics vnc --network bridge=bridge0 --autostart'

print('Current VM List:')
os.system('virsh list --all')

asn = input('VM Owner ASN: AS')
ident = input('Enter VM Identify ID (1-254): ')

vm_name = f'ixvm_{ident}_AS{asn}'

username = input('Enter username of the client: ')
sshkey = input('Enter ssh pubkey of the client: ')

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

virt_inst = virt_inst_temp.format(vmname=vm_name,userdata_path=f'{cwd}/{dirname}/userdata',metadata_path=f'{cwd}/{dirname}/metadata')

print(virt_inst)
os.system(virt_inst)

