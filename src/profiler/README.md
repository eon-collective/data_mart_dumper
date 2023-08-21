# <i>ADEPT Profiler</i>

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
   
   run `docker build --tag adept_profiler:latest .`

2. List images

    run `docker images` to validate docker image exists with name <i>adept_profiler</i> with the latest tag

3. To test running the image, 

    `docker run adept_profiler:latest --version`

    `docker run adept_profiler:latest --help`

    `docker run adept_profiler:latest --input_file_name </path/to/file> --output_location </path/to/output/directory>`


4. To tag and push image to ECR/ Hub etc

```
export IMAGE_TAG=0.8.0
docker build --tag adept_pg_dump_assessor:$IMAGE_TAG .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 745001225527.dkr.ecr.us-east-1.amazonaws.com
docker tag adept_pg_dump_assessor:$IMAGE_TAG 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_pg_dump_assessor:latest
docker tag adept_pg_dump_assessor:$IMAGE_TAG 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_pg_dump_assessor:$IMAGE_TAG
docker push 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_pg_dump_assessor:$IMAGE_TAG
docker push 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_pg_dump_assessor:latest
docker images
```
### To run this application with python

```
python3 run --input_file_name </path/to/file> --output_location </path/to/output/directory>
```

### To run this application with docker

```
Tag the image and push to repo
export IMAGE_TAG=0.0.2
echo $IMAGE_TAG
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 745001225527.dkr.ecr.us-east-1.amazonaws.com
cd src/profiler && docker build . --file Dockerfile --tag adept_profiler:latest --tag adept_profiler:$IMAGE_TAG
docker tag adept_profiler:$IMAGE_TAG 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_profiler:latest
docker tag adept_profiler:$IMAGE_TAG 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_profiler:$IMAGE_TAG
docker push 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_profiler:latest
docker push 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_profiler:$IMAGE_TAG
docker run 745001225527.dkr.ecr.us-east-1.amazonaws.com/adept_profiler:latest --help
```

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
