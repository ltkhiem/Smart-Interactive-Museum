# Smart-Interactive-Museum
-------------------------

# API list

## Create repo

- type: POST
- url: **baseurl**/repo/createrepo
- request: {reponame: string, secret: string}
- response: true/false
## Create class

- type: POST
- url: **baseurl**/repo/**reponame**/createclass
- request: {secret: string, classname: string}
- response: true/false
## Upload file

- type: POST
- url: **baseurl**/repo/**reponame**/**classname**/upload
- body: {img: image file}
## Train class

??? Ask Tien? Train class or train all repo?



## Recognize

- type: POST
- url: **baseurl**/recognize/      ??? => change when use many repo to: **baseurl**/**classname**/recognize
- body: {img: test image, server: tien/anhAn}


What is smart interactive museum?
    - blah blah blah

How to run the project:
    - There are two third-parties, first is Anh An server, Second is One-shot learning API
    - For One-shot learning API configuration:
        - run python setup.py in FaceNet directory for downloading weights
        - in the project directory, run python manage.py runserver
        - Now the server has been deployed, to test it you can request an image to the server by POST/GET method which the body contains the raw bytes of that image attaching with the key 'img'.

