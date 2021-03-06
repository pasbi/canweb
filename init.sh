#!/usr/bin/env bash

cd $(dirname $0)

virtualenv env
source env/bin/activate
pip install -r requirements.txt
./canweb/manage.py migrate

echo 'done. run `./canweb/manage.py runserver` and open your browser at localhost:8000/view/song/list/'