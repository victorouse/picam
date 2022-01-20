#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

# https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/

sudo apt-get update && sudo apt-get upgrade

sudo apt-get install -y build-essential cmake pkg-config

sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev

sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

sudo apt-get install -y libxvidcore-dev libx264-dev

sudo apt-get install -y libfontconfig1-dev libcairo2-dev

sudo apt-get install -y libgdk-pixbuf2.0-dev libpango1.0-dev

sudo apt-get install -y libgtk2.0-dev libgtk-3-dev

sudo apt-get install -y libatlas-base-dev gfortran

sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libhdf5-103

sudo apt-get install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

sudo apt-get install -y python3-dev

wget https://bootstrap.pypa.io/get-pip.py

sudo python get-pip.py

sudo python3 get-pip.py

sudo pip install virtualenv virtualenvwrapper


{ 
  echo "export WORKON_HOME=$HOME/.virtualenvs" 
  echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" 
  echo "export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv" 
  echo "source /usr/local/bin/virtualenvwrapper.sh" 
  echo "export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin" 
} >> ~/.bashrc

source ~/.bashrc

wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.1.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.1.1.zip
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.1.1 opencv
mv opencv_contrib-4.1.1 opencv_contrib

echo "Now time to increase your swapfile size"
echo "Edit: /etc/dphys-swapfile"
echo "Set CONF_SWAPSIZE=2048"
echo "After:"
echo "sudo /etc/init.d/dphys-swapfile stop"
echo "sudo /etc/init.d/dphys-swapfile start"
