package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

// walk dir recursively and run command
func main() {
	dir := os.Getenv("WALKER_DIR")

	const concurrency = 10 // change to 0 to run without concurrency
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
				log.Println("[SKIP]", f.Name())
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

// adjust your code here
func handle(path string) {
	cmd := "python3"
	args := []string{
		"/Volumes/data/playground/face-postgre/face-add.py",
		path,
	}
	execCmd(cmd, args)
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
	}
	fmt.Println("Moved ", from, "to", to)
}
