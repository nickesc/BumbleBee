#!/usr/bin/env sh

deploypath="/Volumes/CIRCUITPY"

#mkdir -p $deploypath/dictionary
#cp -v "dictionary/"*.csv $deploypath/dictionary

#cp -rv "bee_state" $deploypath
#cp -rv "lib" $deploypath
mkdir -p $deploypath/src
cp -rv "src/"*.py $deploypath/src
#cp -v "boot.py" $deploypath
cp -v "code.py" $deploypath

