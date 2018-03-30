#!/usr/bin/env bash

cd $(dirname $0)

virtualenv env
source env/bin/activate
pip -r requirements.txt
./canweb/manage.py migrate

echo "done. run `./canweb/manage.py` and open your browser at localhost:8000/view/song/list/"