#!/bin/sh
export USE_MYSQL='True'
export SECRET_KEY='@+%x+r-cfv@*2+qi)&9w^6jvp-h=bypm+7$uee8jlm1%=qvcjw'
export ENGINE='django.db.backends.mysql'
export NAME='coursebuildercourse$coursebuildercourse'
export USER='coursebuildercourse'
export PASSWORD='releaseit!'
export HOST='coursebuildercourse.mysql.pythonanywhere-services.com'

echo "dollar 1 is $1"

export utilsdir="utils"
#if [ -z "$1" ]
#then
#    utilsdir=$1
#fi
echo "utils dir is $utilsdir"

python3 $utilsdir/qexport.py
