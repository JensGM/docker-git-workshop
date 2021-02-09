#!/bin/bash

set -e

if id -u $1 &>/dev/null; then
    echo user $1 already exists >&2
    exit 1
fi

cmd="useradd -s $(which git-shell)"
home_dir="/home/$1"

if [ ! -d $home_dir ]; then
    cmd="$cmd -m"
else
    cmd="$cmd -d $home_dir"
fi

cmd="$cmd $1"

echo creating user $1 :: $cmd
$cmd
mkdir "$home_dir/.ssh"
