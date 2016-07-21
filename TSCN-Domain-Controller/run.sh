#!/bin/bash


FILEPATH=$(cd "$(dirname "$0")"; pwd)

if [ -f /usr/local/bin/gunicorn ]
    then
    gunicorn_bin=/usr/local/bin/gunicorn
elif
    [ -f /usr/bin/gunicorn ]
    then
    gunicorn_bin=/usr/bin/gunicorn
elif
    [ -f /usr/bin/gunicorn ]
    then
    gunicorn_bin=/opt/mgmt/bin/gunicorn
else
    echo 'Can not find gunicorn binary'
    exit 1
fi

daemon=`echo $1`
if [ "$daemon" == "-D" ]
then
nohup /usr/bin/python $gunicorn_bin app:app_mgmt -c $FILEPATH/gunicorn.conf.py 1>/tmp/app_mgmt.log 2>&1 &
else
/usr/bin/python $gunicorn_bin app:app_mgmt -c $FILEPATH/gunicorn.conf.py
fi