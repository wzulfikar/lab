// Watch for new file in WORKDIR and run alpr.
// USAGE:
// WORKDIR=/Volumes/data/playground/plates COUNTRY=eu go run alprexec.go
package main

import (
	"fmt"
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

	fmt.Println("Scanning directory started")
	go alprgo.ScanDir(workdir, h)

	log.Fatal(alprgo.Watch(workdir, h))
}
