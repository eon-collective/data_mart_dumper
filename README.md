# <i>data_mart_dumper</i>

<img src="https://static.wixstatic.com/media/95af51_ae2122aebc944721a96afd10f3ccfe0c~mv2.png/v1/fill/w_329,h_45,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/95af51_ae2122aebc944721a96afd10f3ccfe0c~mv2.png" alt="drawing" width="200"/><a name="top-">

<p align="center">

[![Pylint](https://github.com/eon-collective/data_mart_dumper/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/eon-collective/data_mart_dumper/actions/workflows/pylint.yml)

</p>

<p align="center">

[![Python application](https://github.com/eon-collective/data_mart_dumper/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/eon-collective/data_mart_dumper/actions/workflows/python-app.yml)

</p>

<p align="center">

[![Docker Image CI](https://github.com/eon-collective/data_mart_dumper/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/eon-collective/data_mart_dumper/actions/workflows/docker-image.yml)

</p>

## Building this project
### Docker image
1. From project root,
   
   run `docker build --tag pg_dumper:latest .`

2. List images

    run `docker images` to validate docker image exists with name <i>pg_dumper</i> with the latest tag

3. To test running the image, 

    `docker run pg_dumper:latest --version`

    `docker run pg_dumper:latest --help`

    `docker run pg_dumper:latest --input_file_name </path/to/file> --output_location </path/to/output/directory>`


## Developing this project
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
