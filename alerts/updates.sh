BASEDIR=$(dirname "$BASH_SOURCE")

set -o allexport && source $BASEDIR/.env && set +o allexport
source $BASEDIR/venv/bin/activate
python $BASEDIR/main.py email=whydontiknowthat@gmail.com should_send=true