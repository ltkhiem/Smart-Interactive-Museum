[![Build Status](https://travis-ci.com/chequochuu/Smart-Interactive-Museum.svg?token=zqCLPftiBUBoP2cktddN&branch=server)](https://travis-ci.com/chequochuu/Smart-Interactive-Museum)
# Smart-Interactive-Museum
-------------------------

# API list

## Create repo

- type: POST
- url: **baseurl**/repo/create_repo/
- request: {name: string, type: string}
- response: true/false

## Create class

- type: POST
- url: **baseurl**/repo/**reponame**/create_class/
- request: {name: string}
- response: true/false

## Upload file

- type: POST
- url: **baseurl**/repo/**reponame**/**classname**/upload/
- body: {img: image file }
- response: fail/success

## Upload zip

- type: POST
- url: **baseurl**/repo/**reponame**/uploadzip/
- body: {data: file.zip}
- response: fail/success

## Train repo

- url: **baseurl**/train/repo/**reponame**/

## Recognize by repo

- type: POST
- url: **baseurl**/recognize/**reponame**/      ??? => change when use many repo to: **baseurl**/**classname**/recognize
- body: {img: test image, server: tien/anhAn}

## Recognize demo

- type: POST
- url: **baseurl**/recognize/demo/
- body: {img: test image}

## Recognize everything

- type: POST
- url: **baseurl**/recognize/everything/
- body: {img: test image}


What is smart interactive museum?
    - blah blah blah

How to run the project:
    - There are two third-parties, first is Anh An server, Second is One-shot learning API
    - For One-shot learning API configuration:
        - run python setup.py in FaceNet directory for downloading weights
        - in the project directory, run python manage.py runserver
        - Now the server has been deployed, to test it you can request an image to the server by POST/GET method which the body contains the raw bytes of that image attaching with the key 'img'.


---------------------
# Deployment
- create a host server with sudo user.

- install anaconda 

wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh

bash Anaconda3-5.1.0-Linux-x86_64.sh

- setting anaconda for bash 

add this line to ~/.bashrc file

export PATH=/home/che/anaconda3/bin:$PATH

- clone project

git clone https://github.com/ltkhiem/Smart-Interactive-Museum.git && cd Smart-Interactive-Museum

- install capstone virtual enviroment by anaconda

conda env create -f environment.yml

- activate capstone enviroment

source activate capstone

- config iptables 

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

- runserver 

python manage.py runserver 0.0.0.0:8080



