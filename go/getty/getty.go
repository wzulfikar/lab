package getty

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/pkg/errors"
)

func urlOk(url string) bool {
	resp, err := http.Head(url)
	if err != nil {
		log.Println("urlOkErr:", err)
		return false
	}
	resp.Body.Close()
	return resp.StatusCode == http.StatusOK
}

// infer name of file from url if filename is empty string ("")
func Get(url, filename, dir string) error {
	if !urlOk(url) {
		return fmt.Errorf("[NOT FOUND] %s", url)
	}

	resp, err := http.Get(url)
	if err != nil {
		return errors.Wrap(err, "GET")
	}
	defer resp.Body.Close()

	// Check server response
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("bad status: %s", resp.Status)
	}

	if filename == "" {
		filename = filepath.Base(url)
	}

	out, err := os.Create(filepath.Join(dir, filename))
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
