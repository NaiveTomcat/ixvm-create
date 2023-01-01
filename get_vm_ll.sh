#!/usr/bin/sh

./mac_to_ipv6_ll.sh $(virsh domiflist $(virsh list --all | grep -ow "ixvm.*AS$1") | grep -ow '52:54:00:.*')
