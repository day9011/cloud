#!/bin/sh
gunicorn -n gamecloud_ui -w 4 main:app -k eventlet -b 0.0.0.0:8000 --max-requests 1000 $1
