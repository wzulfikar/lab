# `entr` requires unix `entr` utility
# → http://entrproject.org
watch-py2 () {
	NC='\033[0;0m' # no color
	GREEN='\033[0;32m'

    FILENAME=$1

    MSG='\n→ Watching python (using entr)..$NC'
    BANNER='${GREEN}Output of $FILENAME:$NC'

    COMMAND="clear && echo '$BANNER' && python3 $FILENAME "

	FILES="find . -name \*.py"

	eval "$FILES | entr sh -c \"$COMMAND; printf '$MSG';\""
}

watch-py3 () {
	NC='\033[0;0m' # no color
	GREEN='\033[0;32m'

    FILENAME=$1

    MSG='\n→ Watching python (using entr)..$NC'
    BANNER='${GREEN}Output of $FILENAME:$NC'

    COMMAND="clear && echo '$BANNER' && python3 $FILENAME "

	FILES="find . -name \*.py"

	eval "$FILES | entr sh -c \"$COMMAND; printf '$MSG';\""
}
