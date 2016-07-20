#!/bin/bash

# install ag
sudo add-apt-repository ppa:pgolm/the-silver-searcher
sudo apt-get update
sudo apt-get install the-silver-searcher

# install ag
sudo apt-get install exuberant-ctags

# install vimrc
cp vimrc ~/.vimrc
# install vim plugins
mkdir -p ~/.vim/bundle/ 
cd ~/.vim/bundle/ 
git clone https://github.com/mileszs/ack.vim.git
git clone https://github.com/kien/ctrlp.vim.git
git clone https://github.com/scrooloose/nerdtree.git
git clone --recursive https://github.com/davidhalter/jedi-vim.git
git clone https://github.com/klen/python-mode.git
git clone https://github.com/tpope/vim-unimpaired.git
git clone https://github.com/scrooloose/syntastic.git
git clone https://github.com/tpope/vim-surround.git
