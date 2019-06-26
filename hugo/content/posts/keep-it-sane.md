---
title: "Keep It Sane"
date: 2019-06-16T03:34:27+08:00
tags: ["workflow", "xp"]
draft: false
# post_id: POST_ID
hideToc: true
# aliases: [
#     "/posts/POST_ID",
# ]
---

This is a list of issues that I've dealt with at least once. The list would serve as a shortcut to save me time from trying to google the solution again and again. It's like index of things that had bitten me in the past.

<!--more-->

The list will be updated from time to time as new issue occurs.

## macOS

<details open>
<summary class="collapsible">collapse</summary>

1. [Source Tree](https://www.sourcetreeapp.com) keep asking for password ([image](/images/macos-sourcetree-keep-asking-for-password.png))
  - **tldr**: `git config --global credential.helper osxkeychain`
  - ref: [stackoverflow](https://stackoverflow.com/questions/38489022/sourcetree-keeps-asking-for-github-password)
- Keychain asking password two times
  - *(Not solved yet)*
- NAS disk prompt keeps popping up
  - *(Not solved yet)*
- Activate "Do Not Disturb" mode (disable all notifications)
  - `alt+click` on notification icon in menu bar. See: [macOS_DnD.mp4](/videos/macOS_DnD.mp4).
- macOS won't boot; grey folder with question mark appears during boot
  - Unfortunately, your SSD might have failed you. Try replacing it.
  - Blog post: WIP

</details>

## Ubuntu

<details open>
<summary class="collapsible">collapse</summary>

1. Stuck in boot screen (Ubuntu's purple screen)
	- Login to [recovery mode](/images/ubuntu-recovery-mode.jpg), run `fsck`, reboot.
- Recover data from unbootable ubuntu
	- Boot to [Finnix rescue cd](https://www.finnix.org/Download), activate ssh server, recover data using sftp. See: [Vultr blog post](https://www.vultr.com/docs/using-finnix-rescue-cd-to-rescue-repair-or-backup-your-linux-system) (or see [snapshot](/images/vultr-finnix-rescue-cd.png)).

</details>

## Android

<details open>
<summary class="collapsible">collapse</summary>

1. [Termux](https://termux.com) can't access device storage
  - Open termux and run `termux-setup-storage`
- Termux history is not active
  - *(Not solved yet)*
- Share termux shell as web app
  - Download [gotty](https://github.com/yudai/gotty), run `./gotty -w sh`, and visit `http://<device-ip>:8080` from browser.

</details>

## Dev

<details open>
<summary class="collapsible">collapse</summary>

1. Debug GraphQL requests in browser
	- Use [GraphQL Network](https://chrome.google.com/webstore/detail/graphql-network/igbmhmnkobkjalekgiehijefpkdemocm?hl=en-GB) extension
- GraphQL error "GROUP BY clause is incompatible with sql_mode=only_full_group_by"
	- Remove 'ONLY_FULL_GROUP_BY' from mysql's `sql_mode`. Example:
	
		```
		SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY,',''));
		```

	- See: [stackoverflow](https://stackoverflow.com/questions/23921117/disable-only-full-group-by)
- Setting git commit author per repo basis
	- run this command in root directory of git repo (based on [dereenigne.org](https://dereenigne.org/git/set-git-email-address-on-a-per-repository-basis/)):
	
	```
	echo "[user]
        name = <author name>
        email = <author oemail>" >> .git/config
	```
- Need to quickly switch proxy server for command line environment
	- use [`proxify.sh`](https://github.com/wzulfikar/lab/blob/master/bash/proxify.sh)
- Preview JSON response in Opera:
	- Install [json-lite](https://addons.opera.com/en/extensions/details/json-lite/) extension
- Save time typing `localhost` by aliasing `l` to `localhost`
  - `echo '127.0.0.1 l' >> /etc/hosts`. `curl l:3000` is now equivalent to `curl localhost:3000`
- Create alias for IP address of hostpot-providing device (Android)
  - `echo '192.168.43.1 android.local' >> /etc/hosts`. See: [stackoverflow](https://stackoverflow.com/questions/17302220/android-get-ip-address-of-a-hotspot-providing-device)
</details>

## Workflow

<details open>
<summary class="collapsible">collapse</summary>

1. Debugging NodeJS, Go, Bash, etc. with vscode
	- *(Blog post in progress)*
- need to grab screen shot and use it as quick reference
	- use grabit
- need to upload file and share it randomly
	- use transfer.sh
- [SublimeText 3](https://www.sublimetext.com/3): show current file in sidebar
	- `ctrl+0` (ctrl+zero). See: [stackoverflow](https://stackoverflow.com/a/15179191/5381120)
- Display full path of file in sublime
  - See: [stackoverflow](https://stackoverflow.com/a/25948759/5381120)
- change command+click handler in iterm (macOS)
  - *(Not solved yet)*
- Convenient scripts:
  - [collate](https://github.com/wzulfikar/lab/blob/master/bash/collate): combine images to one pdf file
  - [makegif](https://github.com/wzulfikar/lab/blob/master/bash/makegif), [makemp4](https://github.com/wzulfikar/lab/blob/master/bash/makemp4): convert videos into (optimized) gif/mp4

</details>

<!-- 
## Others

<details open>
<summary class="collapsible">collapse</summary>

- Can't keep making mistake on opening my washer
	- add glow-in-the dark sticker.
</details>
 -->

 {{< load-photoswipe >}}