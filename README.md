# ADEPT <i> data_mart_dumper <i/>

### Creating a virtual environment in the terminal 
#### macOS/Linux
##### You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs
`python3 -m venv .py-venv`

To activate the environment run
`source .py-venv/bin/activate`

To deactivate the Virtual environment
run `deactivate`

#### Windows
###### You can also use `py -3 -m venv .py-venv`
`python -m venv .py-venv`

To activate the environment run
`.py-venv\Scripts\activate.bat`

To deactivate the Virtual environment
run `deactivate`


##### To display all of the packages installed in the virtual environment
run `python -m pip list`

##### To save all of the packages installed in the virtual environment to a <i>requirements.txt</i>
run `python -m pip freeze > requirements.txt`