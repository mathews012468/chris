set -o allexport && . /app/.env && set +o allexport
python /app/main.py email=whydontiknowthat@gmail.com,$CHRIS_EMAIL phone=$CHRIS_PHONE