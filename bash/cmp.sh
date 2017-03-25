#!/bin/sh
cmp () {
	NC='\033[0m' # no color
	RED='\033[0;31m'
	GREEN='\033[0;32m'
	ORANGE='\033[0;33m'

	echo "Comparing"
	echo "→ $ORANGE$1$NC"
	echo "against"
	echo "→ $ORANGE$2$NC"
	if [ "$1" == "$2" ]
	then
	  	echo "$GREEN✔ MATCH"
	else
		echo "$RED✘ NOT MATCH"
	fi
}
