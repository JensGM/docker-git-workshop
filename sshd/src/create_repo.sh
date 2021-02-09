#!/bin/bash

set -e

user_dir="/home/$1"
repo_dir="$user_dir/$2"

if [ ! -d $user_dir ]; then
    echo directory $user_dir does not exist
    exit 1
fi

if [ -d $repo_dir ]; then
    echo a directory for repo "\"$2\"" already exists "($repo_dir)"
    exit 1
fi

git init --bare $repo_dir
