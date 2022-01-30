#!/bin/bash

PYVER="$(echo $(python -V) | sed 's/Python \(.*\..*\)\..*/\1/')"

sudo apt-get update

sudo apt-get install -y "python${PYVER}-dev" "libpython${PYVER}-dev"
#TODO check if they exist before

#sudo apt-get install -y dpkg-dev build-essential freeglut3-dev libgl1-mesa-dev libglu1-mesa-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev libjpeg-dev libnotify-dev libpng-dev libsdl2-dev libsm-dev libtiff-dev libwebkit2gtk-4.0 libxtst-dev

sudo apt install build-essential python3-pip make gcc libgtk-3-dev libgstreamer-gl1.0-0 freeglut3 freeglut3-dev python3-gst-1.0 libglib2.0-dev ubuntu-restricted-extras libgstreamer-plugins-base1.0-dev

pip install -r requirements.txt
