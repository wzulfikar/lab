package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/wzulfikar/lab/go/getty"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: getty [wordlist] [dir]")
		return
	}

	wordlist := os.Args[1]
	dir := os.Args[2]

	downloadCount := 0 // change to mutex and pass to getasync
	defer func() func() {
		start := time.Now()
		return func() {
			log.Printf("[DONE] Files downloaded: %d. Time elapsed: %s", downloadCount, time.Since(start))
		}
	}()()

	file, err := os.Open(wordlist)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	const concurrency = 5
	sem := make(chan bool, concurrency)

	baseurl := os.Getenv("BASEURL")

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		url := baseurl + scanner.Text() + ".jpeg"
		log.Println("[START]", url)

		sem <- true
		go func(url string) {
			defer func() { <-sem }()
			if err := getty.Get(url, "", dir); err != nil {
				log.Println(err)
			} else {
				downloadCount++
				log.Println("[DONE]", url)
			}
		}(url)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	for i := 0; i < cap(sem); i++ {
		sem <- true
	}
}
