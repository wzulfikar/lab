#!/bin/sh
cmp () {
	echo "Comparing"
	echo "→ $1"
	echo "against"
	echo "→ $2"
	if [ "$1" == "$2" ]
	then
		printf '\033[0;32m'
	  	echo '✔ MATCH'
	else
		printf '\033[0;31m'
		echo '✘ NOT MATCH'
	fi
}
