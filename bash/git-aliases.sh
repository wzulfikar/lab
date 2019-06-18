# aliases for common git operation
alias commit="git commit -m '$1'"
alias add="git add"
alias pull="git pull"
alias push="git push"
alias status="git status"
alias gl="git log --graph --date=format:'%Y-%m-%d %H:%M ❘' --pretty=format:'%Cblue%>(12)%ad %C(yellow)%h %Cgreen%<(7)%aN%Cred%d %Creset%s'"
alias co="git checkout"
alias stash="git stash"
alias rebase="git rebase"
alias reset="git reset"

# quick commit
alias qc="git add . && git commit -m"
