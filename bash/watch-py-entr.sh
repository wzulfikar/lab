# `entr` requires unix `entr` utility
# → http://entrproject.org
watch-py2 () {
	NC='\033[0;0m' # no color
	GREEN='\033[0;32m'

    FILENAME=$1

    MSG='\n→ Watching python (using entr)..$NC'
    BIN="python2"
    COMMAND="clear && echo '${GREEN}Output of ‘$@’:$NC' && $BIN $@"

	FILES="find . -name \*.py"

	eval "$FILES | entr sh -c \"$COMMAND; printf '$MSG';\""
}

watch-py3 () {
	NC='\033[0;0m' # no color
	GREEN='\033[0;32m'

    FILENAME=$1

    MSG='\n→ Watching python (using entr)..$NC'
    BIN="python3"
    COMMAND="clear && echo '${GREEN}Output of ‘$@’:$NC' && $BIN $@"

	FILES="find . -name \*.py"

	eval "$FILES | entr sh -c \"$COMMAND; printf '$MSG';\""
}
