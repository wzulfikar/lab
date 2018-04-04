package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sync"
	"time"
)

func main() {
	workdir := os.Getenv("WORKDIR")
	wordlist := os.Getenv("WORDLIST")

	baseurl := os.Args[1]
	if len(os.Args) < 1 {
		fmt.Println("Usage: getty [baseurl]")
		return
	}

	start := time.Now()
	defer log.Printf("[DONE] Files downloaded: %d. Time elapsed: %s", fileCount, time.Since(start))

	if workdir == "" {
		workdir = "gettyimages"
	}
	if wordlist == "" {
		wordlist = "gettyimages.txt"
	}

	file, err := os.Open(wordlist)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var wg sync.WaitGroup

	fileCount := 0 // change to mutex and pass to getasync
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fileCount++
		wg.Add(1)
		imageUrl := baseurl + scanner.Text()
		log.Println("Downloading", imageUrl)
		go func() {
			defer wg.Done()
			if err := Get(url, filename, dir); err != nil {
				log.Println(err)
			}
		}()
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	wg.Wait()
}
