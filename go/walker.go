package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/pkg/errors"
)

// walk dir recursively and run command
func main() {
	dir := os.Getenv("WALK_DIR")
	concurrency := 5

	fileCount := 0
	defer func() func() {
		start := time.Now()
		return func() {
			fmt.Printf("[DONE] Files walked: %d\n", fileCount)
			fmt.Println("Time elapsed:", time.Since(start))
		}
	}()()

	_ = filepath.Walk(dir, func(path string, f os.FileInfo, err error) error {
		fileCount++
		if f.IsDir() || f.Name() == ".DS_Store" {
			fmt.Println("Not processing dir:", f.Name())
		} else if concurrency == 0 {
			handle(path)
		} else if concurrency > 0 {
			sem := make(chan bool, concurrency)
			sem <- true
			go func(path string) {
				defer func() { <-sem }()
				handle(path)
			}(path)
			for i := 0; i < cap(sem); i++ {
				sem <- true
			}
		}
		return err
	})
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
	log.Println("[START] " + cmdString)

	b, err := exec.Command(cmd, args...).Output()
	if err != nil {
		log.Println(errors.Wrap(err, "exec output"))
	}
	fmt.Println(b)
}

func mv(from, to string) {
	if err := os.Rename(from, to); err != nil {
		log.Println("mv failed:", err)
	}
	fmt.Println("Moved ", from, "to", to)
}
