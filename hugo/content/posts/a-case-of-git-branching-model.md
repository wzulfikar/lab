---
title: "A Case of Git Branching Model"
date: 2018-04-12T18:08:45+08:00
tags: [""]
draft: true
---

`TODO: write content` 


```
▾ master
  ▾ hotfix
    ‣ hotfix 1
      ⚑ pull request to master
        - code review
        - merge hotfix to master
        - merge master to develop
    ‣ hotfix 2
      ..[redacted]..
    ‣ hotfix n
      ..[redacted]..
  ▾ develop
    ⚑ pull request to master
      - test develop branch in staging
      - merge develop to master
      - tag the merge with new release version
    ‣ feature 1
      ⚑ pull request to develop
        - sync with develop using git rebase
        - code review for the feature
        - test the feature
        - merge feature to develop
    ‣ feature 2
      ..[redacted]..
    ‣ feature n
      ..[redacted]..
```



<p class="text-center">***</p>

*Outline:*

1. https://datasift.github.io/gitflow/IntroducingGitFlow.html
2. don't rebase shared branch (master, develop). rebase feature branch only (if the feature it's being worked by individu, not shared)
3. graphical difference between merge & rebase 
4. pushing *rebased* feature branch to server
