---
title: "I Forgot My Keepass Master Password"
date: 2019-04-01T18:36:08+08:00
draft: true
tags: [security, hashcat, password manager]
---

Today was just like another day, until I realized that I can't open my keepass password manager. Apparently, I forgot my master password.

<!--more-->

Keepass is an open source password manager (see: https://keepass.info) that offers similar features of other password managers like keychain (macOS), lastpass.com (online), etc. If you have never seen Keepass before, check this video.

{{< youtube grf_LyudTE0 >}}

</br>

Here's what happens in the video:

1. Open "Keepass" app (I'm running Ubuntu 18.04)
2. Create new keepass db at `~/Desktop/Database.kdbx` and save it
3. Insert master password for the new keepass db
4. Insert name for the db (I named it `MyDatabase`)
5. Add new login entry "**Some Login**" (in real life, this can be website login, etc.)
6. Lastly, save the changes I made to my keepass

The steps in the video should give you some context on how Keepass works. You store your password in Keepass, and Keepass will store it securely in keepass db (in our case, it's `~/Desktop/Database.kdbx`).

It's considered secure because the db file is encrypted with the master password: the content of keepass db won't be accessible (won't be decrypted) until the corect master password is supplied. Losing/forgetting master password means losing all your stored logins.

I don't want to go through "forget password" routine of every website or services that I used. So, instead of giving up, I kept trying to insert whatever password I remember. _No luck._

![keepass wrong master password](/images/keepass-wrong-password.gif)

asdfaf

![sample password list](/images/keepass-password-list-hashcat.png)



![hashcate keepass hashmode 13400](/images/hashcat-hashmode-keepass-13400.png)


![extract hash from keepass db](/images/extract-hash-from-keepass-db.png)



![extract hash from keepass db](/images/hashcat-error-need-force.png)

![extract hash from keepass db](/images/hashcat-completed.png)

![extract hash from keepass db](/images/hashcat-subsequent-run.png)

![extract hash from keepass db](/images/hashcat-password-from-potfile.png)


![extract hash from keepass db](/images/hashcat-potfile-content.png)
