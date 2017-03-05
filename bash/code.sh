# just alias to directory for code stuffs,
# eg. `~/code/web`, `~/code/mobile-app`, etc.
code () {
  if [[ $1 ]]; then
    eval "cd ~/code/$1"
  else
    eval "cd ~/code"
  fi
}
