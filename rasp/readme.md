# Install Raspberry packages from rasp_init.sh by 
chmod +x rasp_init.sh
./rasp_init.sh

# Install virtual environment
python3 -m pip install virtualenv

# Create a new virtual environment
python3 -m venv virtualenv

# Activate it
source virtualenv/bin/activate

# Update pip
python3 -m pip install --upgrade pip

# Install tensorflow
wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl

python3 -m pip install tensorflow-2.4.0-cp37-none-linux_armv7l.whl

# Install packages
python3 -m pip install -r requirements.txt 
