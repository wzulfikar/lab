---
title: "Gotcha!"
date: 2019-06-25T20:26:16+08:00
tags: ["programming"]
draft: false
hideToc: true
#post_id: POST_ID
#aliases: [
#	"/posts/POST_ID",
#]
---

Collection of programming gotchas I have personally encountered. And made me confused.

<!--more-->

# Shell

<details open>
<summary class="collapsible">collapse</summary>

1. `echo` vs `echo -n`. Use the latter if you want to check for hash.

	{{< highlight bash "linenos=table" >}}
echo "hello world" | shasum -a 256 		# trailing newline is included in hash
echo -n "hello world" | shasum -a 256 	# use -n to exclude trailing newline{{< / highlight >}}

	{{< show-repl-it url="https://repl.it/@wzulfikar/shell-gotcha-echo?lite=true" >}}

</details>

# JS

<details open>
<summary class="collapsible">collapse</summary>

1. Watch out for [control characters'](https://en.wiktionary.org/wiki/Appendix:Control_characters) padding when encoding to hex.

	{{< highlight php "linenos=table" >}}
const controlChar = '\n'
const hex = Buffer.from(controlChar).toString('hex')
hex == controlChar.charCodeAt(0).toString(16)					// false
hex == controlChar.charCodeAt(0).toString(16).padStart(2, '0')	// true{{< / highlight >}}

	{{< show-repl-it url="https://repl.it/@wzulfikar/js-gotcha-char-code?lite=true" >}}

</details>
