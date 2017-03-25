# run ubuntu bash shell
alias ubuntu="docker run -it --rm phusion/baseimage bash"

# `docker ps` format string for vertical display
export DOCKER_PS_FORMAT="ID\t{{.ID}}\nNAME\t{{.Names}}\nIMAGE\t{{.Image}}\nPORTS\t{{.Ports}}\nCOMMAND\t{{.Command}}\nCREATED\t{{.CreatedAt}}\nSTATUS\t{{.Status}}\n"
