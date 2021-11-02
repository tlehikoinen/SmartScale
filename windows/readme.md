# Windows setup

### Setup virtual environment
python3 -m pip install virtualenv  
python3 -m venv virtualenv  
.\virtualenv\Scripts\activate  
python3 -m pip install --upgrade pip   

### Setup with Tensorflow 2.5.0
python3 -m pip install -r .\windows\requirements.txt   
python3 -m ipykernel install --user --name=virtualenv  

### Setup with Tensorflow lite runtime
wget https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp37-cp37m-win_amd64.whl  
python3 -m pip install tflite_runtime-2.5.0.post1-cp37-cp37m-win_amd64.whl   
python3 -m pip install -r .\windows\literequirements.txt  







