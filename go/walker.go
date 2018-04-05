// walk dir recursively and run command
package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

// adjust your code here
func handle(path string) {
	cmd := "python3"
	args := []string{
		"/Volumes/data/playground/face-postgre/face-add.py",
		path,
	}
	execCmd(cmd, args)

	filename := filepath.Base(path)
	mv(path, "/data/processed-images/"+filename)
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("USAGE : walker [dir] [concurrency]")
		fmt.Println("SAMPLE: walker ~/data/images 10")
		return
	}
	dir := os.Args[1]
	concurrency, err := strconv.Atoi(os.Args[2])
	if err != nil {
		log.Fatal(err)
	}

	log.Println("[INIT] Walking directory", dir, "with", concurrency, "concurrency")

	sem := make(chan bool, concurrency)

	fileCount := 0
	defer func() func() {
		start := time.Now()
		return func() {
			log.Println("[DONE] Files walked:", fileCount)
			fmt.Println("Time elapsed:", time.Since(start))
		}
	}()()

	_ = filepath.Walk(dir, func(path string, f os.FileInfo, err error) error {
		if err != nil {
			fmt.Println("filepath error:", err)
		} else {
			fileCount++
			log.Printf("Processing file #%d: %s\n", fileCount, f.Name())

			if f.IsDir() || f.Name() == ".DS_Store" {
				log.Println("[SKIP]", path)
			} else if concurrency == 0 {
				handle(path)
			} else if concurrency > 0 {
				sem <- true
				go func(path string) {
					defer func() { <-sem }()
					handle(path)
				}(path)
			}
		}
		return err
	})

	if concurrency > 0 {
		for i := 0; i < cap(sem); i++ {
			sem <- true
		}
	}
}

func execCmd(cmd string, args []string) {
	cmdString := cmd + " " + strings.Join(args, " ")
	log.Println("[START]", cmdString)

	b, err := exec.Command(cmd, args...).Output()
	if err != nil {
		log.Println("exec output error:", err)
	}
	fmt.Printf("%s\n", b)
}

func mv(from, to string) {
	if err := os.Rename(from, to); err != nil {
		log.Println("mv failed:", err)
		return
	}
	fmt.Println("[MOVE]", from, "to", to)
}

func rm(path string) {
	if err := os.Remove(path); err != nil {
		log.Println("rm failed:", err)
		return
	}
	fmt.Println("[REMOVE]", path)
}
