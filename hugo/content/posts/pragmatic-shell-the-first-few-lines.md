---
title: "Pragmatic Shell: First Few Lines"
date: 2019-03-16T18:42:14+08:00
tags: [""]
draft: true
---

One of few lines I like to begin my shell script with is the lines that will display "usage" info: a one-liner of what the script is, how to use the script, and some examples.

"sometimes, the hardest part is to start"

<!-- more -->

# Motive


style="font-weight: 300; border-bottom: 2px solid #8a8a8a;"

Here is some sample code taken from my `len` script (available at [github](https://github.com/wzulfikar/lab/tree/master/bash/len)):

after encoding the 

{{< highlight sh "linenos=table" >}}
#!/usr/bin/env sh

if [ -z "$1" ]; then
    echo "len –– get length of passed argument (ie. string)"
    echo "usage: len <string>"
    exit
fi
{{< / highlight >}}


*Outline:*

1. 