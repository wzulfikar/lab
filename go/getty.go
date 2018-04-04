package getty

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"sync"
)

func urlOk(url string) bool {
	resp, err := http.Head(url)
	if err != nil {
		return false
	}

	return resp.StatusCode == http.StatusOK
}

func GetAsync(dir, url string, wg *sync.WaitGroup) {
	defer wg.Done()
	if err := get(dir, url); err != nil {
		log.Println(err)
	}
}

func Get(dir, url string) error {
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
