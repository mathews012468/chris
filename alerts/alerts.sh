#set environment vars from file as indicated by this answer:
#https://stackoverflow.com/a/30969768
set -o allexport && . /app/.env && set +o allexport
/usr/local/bin/python /app/main.py email=whydontiknowthat@gmail.com,$CHRIS_EMAIL phone=$CHRIS_PHONE