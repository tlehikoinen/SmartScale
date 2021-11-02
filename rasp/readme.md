# Raspberry Pi 4 setup
### Install Raspberry packages from rasp_init.sh    
chmod +x rasp_init.sh  
./rasp_init.sh  

### Setup virtual environment
python3 -m pip install virtualenv  
python3 -m venv virtualenv  
source virtualenv/bin/activate  
python3 -m pip install --upgrade pip  

## Tensorflow
##### Install tensorflow and requirements
wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl    
python3 -m pip install tensorflow-2.4.0-cp37-none-linux_armv7l.whl   
python3 -m pip install -r ./rasp/requirements.txt   

## Tensorflow lite runtime
wget https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp37-cp37m-linux_armv7l.whl   
python3 -m pip install tflite_runtime-2.5.0.post1-cp37-cp37m-linux_armv7l.whl   
python3 -m pip install -r ./rasp/literequirements.txt   



