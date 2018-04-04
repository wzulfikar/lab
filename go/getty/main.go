package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sync"

	"github.com/wzulfikar/lab/go/getty"
)

func main() {
	workdir := os.Getenv("WORKDIR")
	wordlist := os.Getenv("WORDLIST")

	baseurl := os.Args[1]
	if len(os.Args) < 1 {
		fmt.Println("Usage: getty [baseurl]")
		return
	}

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
		go getty.GetAsync(workdir, imageUrl, &wg)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	wg.Wait()
	log.Println("Files downloaded:", fileCount)
}
