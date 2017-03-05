runcpp () {
    FILENAME=$1
    eval "g++ -o $FILENAME $FILENAME.cpp && ./$FILENAME"
}

// `watchmedo` requires watchdog (python) 
// → https://pythonhosted.org/watchdog
watchcpp () {
    FILENAME=$1
    COMMAND="echo \ && g++ -o $FILENAME $FILENAME.cpp && ./$FILENAME"

    echo "Watching $1.cpp file.."

    eval "watchmedo shell-command \
        --patterns='*.cpp' \
        --command='$COMMAND \n' \
        ."
}
