package main

import (
	"log"
	"os"

	alprgo "github.com/wzulfikar/lab/go/alpr"
)

func main() {
	workdir := os.Getenv("WORKDIR")
	adjustStdout := true
	country := "eu"
	processedImagesPath := "processed"

	h := alprgo.NewExecHandler(adjustStdout, country, processedImagesPath)
	log.Fatal(alprgo.Watch(workdir, h))
}
