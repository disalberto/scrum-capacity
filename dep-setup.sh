#!/bin/bash

PYVER="$(echo $(python -V) | sed 's/Python \(.*\..*\)\..*/\1/')"

sudo apt-get install -y "python${PYVER}-dev" "libpython${PYVER}-dev" 
#TODO check if they exist before

sudo apt-get install -y dpkg-dev build-essential freeglut3-dev libgl1-mesa-dev libglu1-mesa-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev libjpeg-dev libnotify-dev libpng-dev libsdl2-dev libsm-dev libtiff-dev libwebkit2gtk-4.0-dev libxtst-dev

pip install -r requirements.txt