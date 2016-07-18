#!/bin/bash

if [ $# -ne 2 ] && [ $# -ne 3 ]; then
    cat <<EOD
Usage:
  $0 username hostname [newhostname]

EOD
    exit 1
fi

user="$1"
shift
reboothost="$1"
shift
waithost="$1"
[ "$waithost" = "" ] && waithost="$reboothost"

ssh "$user@$reboothost" sudo reboot
sleep 5
n=0
cmd="ping -c 1 -W 1 $waithost"
while ! $cmd > /dev/null 2>&1; do
    if [ $n -eq 0 ]; then
        echo -n "waiting for $waithost to be pingable "
    else
        echo -n "."
    fi  
    sleep 1 
    let n+=1
done
echo "$waithost pingable..."

n=0
cmd="ssh $user@$waithost exit"
while ! $cmd > /dev/null 2>&1; do
    if [ $n -eq 0 ]; then
        echo -n "waiting for ssh to come up for $user@$waithost "
    else
        echo -n "."
    fi  
    sleep 1 
    let n+=1
done
echo "ssh connection possible"

