#!/bin/bash

env='/opt/ops-env/bin/activate'
project_home='/opt/AliyunCenter/'

source $env
cd $project_home

startup(){
    # Celery
    nohup celery -A AliyunCenter worker -l info -Q for_task_setCache -n for_task_setCache.%h --pidfile=/var/run/c_celery_worker.pid >> /var/log/c_celery-worker.log 2>&1 &
    nohup celery -A AliyunCenter worker -l info -Q for_task_search -n for_task_search.%h --pidfile=/var/run/s_celery_worker.pid >> /var/log/s_celery-worker.log 2>&1 &
    nohup celery -A AliyunCenter beat -l info --pidfile=/var/run/celery_beat.pid >> /var/log/celery-beat.log 2>&1 &

    # gunicorn
    gunicorn AliyunCenter.wsgi -c gunicorn.conf
}

shutdown(){
    kill `cat /var/run/c_celery_worker.pid`
    kill `cat /var/run/s_celery_worker.pid`
    kill `cat /var/run/celery_beat.pid`
    kill `cat /var/run/gunicorn.pid`
}



case $1 in
    start)
        startup;;
    stop)
        shutdown;;
    *)  
        echo 'Usage: statr | stop';;
esac
