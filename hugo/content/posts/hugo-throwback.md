---
title: "Hugo Throwback"
date: 2018-11-03T02:33:20+08:00
tags: ["experiment", "go"]
draft: true
enableToc: false
---

1. using hugo-theme-cactus-plus
    - enable tags by:
        1. adding `tag` in `taxonomies` in config file, ie.

        ```
        [taxonomies]
            tag = "tags"
        ``` 
        2. add `tags` in page's frontmatter. ie. `tags = ["go"]`
        3. visit posts by tags from `/tags/go`