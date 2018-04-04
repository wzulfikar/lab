package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"sync"
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
		go getAsync(workdir, imageUrl, &wg)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	wg.Wait()
	log.Println("Files downloaded:", fileCount)
}

func urlOk(url string) bool {
	resp, err := http.Head(url)
	if err != nil {
		return false
	}

	return resp.StatusCode == http.StatusOK
}

func getAsync(dir, url string, wg *sync.WaitGroup) {
	defer wg.Done()
	if err := get(dir, url); err != nil {
		log.Println(err)
	}
}

func get(dir, url string) error {
	if !urlOk(url) {
		return fmt.Errorf("[NOT FOUND] %s", url)
	}

	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Check server response
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("bad status: %s", resp.Status)
	}

	file := filepath.Base(url)
	out, err := os.Create(filepath.Join(dir, file))
	if err != nil {
		return err
	}
	defer out.Close()

	// Writer the body to file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return err
	}

	return nil
}
