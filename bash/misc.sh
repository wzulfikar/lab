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

# edit zsh config
alias zshconfig="sudo nano ~/.zshrc"

# update zsh config
alias zshso="source ~/.zshrc" # 

# edit hosts config using sublime text
alias hostsconfig="subl /etc/hosts"

# laravel artisan
alias artisan="php artisan" 

# python alias
alias py2=python2
alias py3=python3
