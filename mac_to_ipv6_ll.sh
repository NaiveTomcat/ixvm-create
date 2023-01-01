#!/bin/bash

IFS=':'; set $1; unset IFS
printf "fe80::%x%x:%x:%x:%x\n" $(( 0x${1} ^ 0x02 )) 0x${2} 0x${3}ff 0xfe${4} 0x${5}${6}
