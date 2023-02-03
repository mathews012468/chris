BASEDIR=$(dirname "$BASH_SOURCE")

set -o allexport && source $BASEDIR/.env && set +o allexport
python3 $BASEDIR/updateNumber.py