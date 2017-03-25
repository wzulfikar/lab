# Alias to directory for code stuffs (personal preference). 
# Type `code` in your terminal and it will bring you to 
# the directory where you place your codes. This way, 
# you can jump to your code directly from anywhere in 
# your terminal which can help reduce mental burden. 
code () {
	CODE_DIRECTORY="~/code"
	if [[ $1 ]]; then
    	eval "cd $CODE_DIRECTORY/$1"
	else
    	eval "cd $CODE_DIRECTORY"
  	fi
}

# get length of whatever passsed in
len () {
	NC='\033[0m' # no color
	GREEN='\033[0;32m'
	ORANGE='\033[0;33m'
	echo "Length of $ORANGE'$1'$NC is$GREEN ${#1}"
}
