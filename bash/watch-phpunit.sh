watch-phpunit () {
    echo "Watching php file for test.."

    if [[ $1 ]]; then
      eval "watchmedo shell-command \
          --patterns='*.php' \
          --recursive \
          --command='vendor/bin/phpunit $1' \
          ."
    else
      eval "watchmedo shell-command \
          --patterns='*.php' \
          --recursive \
          --command='vendor/bin/phpunit' \
          ."
    fi
}
