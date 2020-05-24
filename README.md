# Decode_Hisense_Aircond
Decode and transmit Hisense Aircond IR codes using RPi and LIRC

## Prerequisites
### External Python Libraries
Update PIP
```
python -m pip install --upgrade pip
```
Install required libraries
```
pip install virtualenv
```

## Setup
### Workspace Creation 
Navigate to new workspace folder
```
cd path/to/workspace
```

### Download from Git
```
git clone https://github.com/Palt0n/kh-serverstats.git
```

### Setup python virtual environment with venv
Create python virtual enviroment with venv
```
python -m venv env
```
To activate venv
```
source env/Scripts/activate
```
To check if venv is activated

```
which python
```
- This command should return the path for python.
- This path should be located in the local env folder

If you want to exit venv later (DONT EXIT NOW!), use
```
deactivate
```
### Download external python libraries
Have to repeat the pip upgrade in venv
```
python -m pip install --upgrade pip
```

Ensure that venv is activated, then install the libararies using pip
```
pip install -r requirements.txt
```
Or run 
```
pip install numpy
pip install matplotlib
```

## Run
To obtain Y for X values
```
python plot_mode2.py
```
Adjust value until a good R squared value is obtained

Once good values are obtain, edit `parse_mode2.py` with the new values and run:
```
python parse_mode2.py Hisense_Aircond_Power.mode2.example
```

## Developer Misc
### Create requirements.txt file
```
pip freeze > requirements.txt
```
