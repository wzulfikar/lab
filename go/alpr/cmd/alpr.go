package main

import (
	"log"
	"os"

	alprgo "github.com/wzulfikar/lab/go/alpr"
)

func main() {
	path := os.Getenv("ALPR_PATH")
	log.Fatal(alprgo.Watch(path, &alprgo.DefaultAlprHandler{}))
}
