#!/bin/sh

cd ./model_chooser/ && source ./bin/activate
pip install -r requirements.txt
python3 app.py
