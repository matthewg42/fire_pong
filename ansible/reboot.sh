#!/bin/bash

if [ $# -eq 2 ]; then
    user="$1"
    host="$2"
    newuser="$1"
    newhost="$2"
elif [ $# -eq 4 ]; then
    user="$1"
    host="$2"
    newuser="$3"
    newhost="$4"
else
    cat <<EOD
Usage:
  $0 username hostname [newuser newhost]

EOD
    exit 1
fi

if [ "$user" != "root" ]; then
    ssh "$user@$host" sudo reboot
else
    ssh "$user@$host" reboot
fi
sleep 5

n=0
cmd="ping -c 1 -W 1 $newhost"
while ! $cmd > /dev/null 2>&1; do
    if [ $n -eq 0 ]; then
        echo -n "waiting for $newhost to be pingable "
    else
        echo -n "."
    fi  
    sleep 1 
    let n+=1
done
echo "$newhost pingable..."

n=0
cmd="ssh $newuser@$newhost exit"
while ! $cmd > /dev/null 2>&1; do
    if [ $n -eq 0 ]; then
        echo -n "waiting for ssh to come up for $newuser@$newhost "
    else
        echo -n "."
    fi  
    sleep 1 
    let n+=1
done
echo "ssh connection possible"

