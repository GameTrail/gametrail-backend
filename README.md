# GameTrail API 


# Setup guide

## Run locally

- Install virtualenv `pip install virtualenv`
- Create a project directory `mkdir gametrail-env`
- Move to env directory with `cd gametrail-env`
- Create virtual enviroment `virtualenv venv -p python3.11`
- Activate virtual enviroment
    - **(MacOS)** with `source venv/bin/activate` 
    - **(Windows)** follow this guide https://linuxhint.com/activate-virtualenv-windows/
- Clone gametrail-backend repository `git clone https://github.com/GameTrail/gametrail-backend.git`
- Move to gametrail repo with `cd gametrail-backend`
- Install project dependencies `pip install -r requirements.txt`
- Migrate the app `./manage.py makemigrations` & `./manage.py migrate`
- Run the API `./manage.py runserver`
- Access to the DEMO API on `http://127.0.0.1:8000/demoapi/`
