#!/bin/bash

sudo apt-get install build-essential cmake
sudo apt-get install python-dev python3-dev

git clone https://github.com/Valloric/YouCompleteMe.git
cd ~/.vim/bundle/YouCompleteMe
git submodule update --init --recursive
./install.py
