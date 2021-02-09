#!/bin/bash

set -e

user_dir="/home/$1"
repo_dir="$user_dir/$2"

if [ ! -d $user_dir ]; then
    echo directory $user_dir does not exist
    exit 1
fi

if [ ! -d $repo_dir ]; then
    echo directory $repo_dir does not exist
    exit 1
fi

rm -rf $repo_dir
