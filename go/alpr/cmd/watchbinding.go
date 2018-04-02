// Watch for new file in WORKDIR and run alpr.
// USAGE:
// WORKDIR=/Volumes/data/playground/plates COUNTRY=eu go run watchbinding.go
package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/openalpr/openalpr/src/bindings/go/openalpr"
	alprgo "github.com/wzulfikar/lab/go/alpr"
)

func main() {
	defer func() {
		if err := recover(); err != nil {
			fmt.Errorf("panic: %v", err)
			time.Sleep(2 * time.Second)
			loop()
		}
	}()
	loop()
}

func loop() {
	// directory for alpr runtime data. ie,
	// /usr/local/share/openalpr/runtime_data
	workdir := os.Getenv("WORKDIR")
	runtimeDir := os.Getenv("RUNTIME_DIR")
	country := os.Getenv("COUNTRY")
	config := os.Getenv("CONFIG")

	h := alprgo.NewBindingHandler(country, config, runtimeDir)
	if !h.Alpr.IsLoaded() {
		fmt.Println("OpenAlpr failed to load!")
		return
	}
	defer h.Alpr.Unload()
	h.Alpr.SetTopN(20)

	fmt.Println("OpenAlpr started. Version:", openalpr.GetVersion())

	fmt.Println("Scanning directory started")
	go alprgo.ScanDir(workdir, h)

	log.Fatal(alprgo.Watch(workdir, h))
}
