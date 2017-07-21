# aliases for common git operation
alias commit="git commit -m '$1'"
alias add="git add"
alias pull="git pull"
alias pull2="git checkout master & git pull & git checkout develop & git pull"
alias push="git push"
alias push2="git checkout master & git push & git checkout develop & git push"
alias status="git status"
alias gitlog="git log --one-line --graph -n 10"

# quick commit
alias qc="git add . && git commit -m"