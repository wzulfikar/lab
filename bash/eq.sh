#!/bin/sh
eq () {
	NC='\033[0m' # no color
	RED='\033[0;31m'
	GREEN='\033[0;32m'
	ORANGE='\033[0;33m'


	if [ "$1" = "$2" ]
	then
		echo "${GREEN}[IT EQUALS!]${NC}\n"
		IS_EQUAL_TEXT="${GREEN}▍IS EQUAL TO"
	else
		echo "${RED}[NOT EQUALS!]${NC}\n"
		IS_EQUAL_TEXT="${RED}▍IS NOT EQUAL TO"
	fi

	echo "▍$1\n$IS_EQUAL_TEXT\n${NC}▍$2"
}
