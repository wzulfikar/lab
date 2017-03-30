# NOTE: watchdog must be installed.
# eg: `watchartisan list` will execute 
# `php artisan list` everytime there's change in `*.php` files
watch-artisan () {
	NC='\033[0;0m' # no color
	ORANGE='\033[0;33m'

    MSG='$ORANGE→ Watching php files to run artisan command (using entr)..$NC'

	FILES="find . -name \*.php -not -path './vendor/*'"
	COMMAND="clear && php artisan $1"

	eval "$FILES | entr sh -c \"$COMMAND; printf '$MSG'\""
}
