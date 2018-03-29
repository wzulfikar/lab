# Download big file from google drive using curl. 
# Taken from: 
# https://gist.github.com/tanaikech/f0f2d122e05bf5f971611258c22c110f
# Dependencies: 
# Golang pup (https://github.com/ericchiang/pup)
gdriveget() {
	FILEID=$1
	FILENAME=$2

	if [ -z $FILEID ]; then
	    echo "Please provide google drive file id as first argument"
	elif [ -z $FILENAME ]; then
	    echo "Please provide filename as second argument"
	elif ! type "pup" > /dev/null; then
	    echo "pup command is not available. Please get it from https://github.com/ericchiang/pup"
	else
		query=`curl -c ./cookie.txt -s -L "https://drive.google.com/uc?export=download&id=${FILEID}" | pup 'a#uc-download-link attr{href}' | sed -e 's/amp;//g'`
		curl -b ./cookie.txt -L -o ${FILENAME} "https://drive.google.com${query}"
	fi
}