# `entr` requires unix `entr` utility
# → http://entrproject.org
watch-go () {
	NC='\033[0;0m' # no color
	GREEN='\033[0;32m'

    FILENAME=$1

    MSG='\n→ Watching go (using entr)..$NC'
    BANNER='${GREEN}Output of $FILENAME:$NC'

    COMMAND="clear && echo '$BANNER' && go run $FILENAME"

	FILES="find . -name \*.go"

	eval "$FILES | entr sh -c \"$COMMAND; printf '$MSG';\""
}
