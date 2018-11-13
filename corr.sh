#!/bin/bash
dbwebb run potatoe $3 && dbwebb -y inspect $1 $2 $3
python3 js1-kmom01.py $3
