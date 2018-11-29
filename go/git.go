package main

import (
	"log"
	"strings"

	"github.com/wzulfikar/lab/go/yell"
)

func main() {
	out, err := yell.Yell("git", "describe", "--always")
	if err != nil {
		if strings.Contains("not a git repository", out.String()) {
			log.Fatal("directory is not a git repo")
			return
		}
		log.Fatal(err)
	}

	// spew.Dump(out)
	log.Printf(out.String())
}
