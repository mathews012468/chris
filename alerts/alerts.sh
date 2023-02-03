BASEDIR=$(dirname "$BASH_SOURCE")

set -o allexport && . $BASEDIR/.env && set +o allexport
. $BASEDIR/venv/bin/activate
python $BASEDIR/main.py email=whydontiknowthat@gmail.com,$CHRIS_EMAIL phone=$CHRIS_PHONE