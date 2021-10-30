#!/bin/sh

sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 \
                        libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev \
                        liblapack-dev cython3 libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev \
			build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev \
			libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
			libxvidcore-dev libx264-dev \
			libfontconfig1-dev libcairo2-dev \
			libgdk-pixbuf2.0-dev libpango1.0-dev \
			libgtk2.0-dev libgtk-3-dev \
			libatlas-base-dev gfortran \
			libhdf5-dev libhdf5-serial-dev libhdf5-103 \
			libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 


sudo pip3 install pip --upgrade
pip3 install -U --user six wheel mock


