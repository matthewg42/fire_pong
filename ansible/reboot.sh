#!/bin/bash

if [ $# -ne 2 ]; then
    cat <<EOD
Usage:
  $0 username hostname 

EOD
    exit 1
fi

ssh "$1@$2" sudo reboot
sleep 5
n=0
cmd="ping -c 1 -W 1 $2"
while ! $cmd > /dev/null 2>&1; do
    if [ $n -eq 0 ]; then
        echo -n "waiting for $2 to be pingable "
    else
        echo -n "."
    fi  
    sleep 1 
    let n+=1
done
echo "$2 pingable..."

n=0
cmd="ssh $1@$2 exit"
while ! $cmd > /dev/null 2>&1; do
    if [ $n -eq 0 ]; then
        echo -n "waiting for ssh to come up for $1@$2 "
    else
        echo -n "."
    fi  
    sleep 1 
    let n+=1
done
echo "ssh connection possible"

