# Smart scale
On going project about Smart scale that automatically predicts the item being weighed.

Python version 3.7.3
## Windows
### Setup
1. python3 -m pip install virtualenv  
2. python3 -m venv virtualenv
3. .\virtualenv\Scripts\activate  
4. python3 -m pip install --upgrade pip
4. python3 -m pip install -r .\windows\requirements.txt  
5. python3 -m ipykernel install --user --name=virtualenv

## Raspberry Pi 4 (OS version 3.5.0)
### Setup
chmod +x ./rasp/rasp_init.sh
./rasp/rasp_init.sh

python3 -m pip install virtualenv
python3 -m venv virtualenv
source virtualenv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r ./rasp/requirements.txt
